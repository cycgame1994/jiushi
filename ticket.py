import random
import json
from datetime import datetime, time as dt_time
from re import S
from curl_cffi.requests import AsyncSession
import asyncio
import requests
from config import (
    url_a,
    url_j,
    url_b,
    url_h,
    url_k,
    url_e,
    url_c,
    webhook_url,
    webhook_url2,
    webhook_url3,
    headers,
    ACCOUNT_POOL,
)
from proxy_config import get_proxy_dict, proxy_updater_task, force_refresh_proxy

"""
1.增加代理ip,轮询请求网址 √
2.增加每天定时启动，关闭发送请求 √
4.增加统计功能，监控到有票后，统计每一种票的出现次数，发送到钉钉消息
5.失败重试机制，每5次失败发送推送消息到ios的bark
6.按照a,j,d,b,h,k,e,c的顺序请求，每一轮发送钉钉消息，而不是每一次请求发一次，并且消息中带有时间戳
7，为后续和手机的autox自动抢票做准备，检测到有票后，发送websocket信息给手机的autox
"""
# 运行状态控制
is_running = False  # 全局运行标志
running_lock: asyncio.Lock = None  # 运行状态锁

# Bark 基础配置（用于账号封禁 & 熔断 start/stop 通知）
BARK_BASE_URL = "https://api.day.app/BWhqdkST7VWwSj3HU5tbRo"

# 熔断/软封禁控制配置
# 连续触发 Bark 次数达到该值后触发熔断
SOFTBAN_BARK_THRESHOLD = 7

# 熔断暂停时间（秒）
# - 放票/高峰期：暂停 20 秒
# - 空闲期：暂停 40 秒
# 后期如果需要调整，只需修改下面两个值即可
PAUSE_DURATION_SECONDS_ACTIVE = 40  # 放票/高峰期
PAUSE_DURATION_SECONDS_IDLE = 40    # 空闲期

# 熔断状态
softban_bark_count = 0             # 当前累计的 Bark 次数（用于软封禁判断）
pause_in_progress = False          # 是否已经在执行暂停流程，避免重复触发
softban_active = False             # 是否处于软封禁熔断期（为 True 时强制不运行）
softban_lock: asyncio.Lock = None  # 熔断计数锁

# 定时配置
START_TIME = dt_time(4, 0, 0)   # 启动时间
END_TIME = dt_time(23, 59, 59)  # 结束时间
STATS_TIME = dt_time(22, 0, 0)  # 统计消息发送时间


def is_within_running_window(now: datetime | None = None) -> bool:
    """
    判断当前时间是否在配置的运行窗口内。
    运行时间：START_TIME 到 END_TIME（含边界）。
    """
    if now is None:
        now = datetime.now()
    current_time = now.time()
    return START_TIME <= current_time <= END_TIME


def get_running_lock():
    """获取或创建运行状态锁"""
    global running_lock
    if running_lock is None:
        running_lock = asyncio.Lock()
    return running_lock


def get_softban_lock():
    """获取或创建熔断计数锁"""
    global softban_lock
    if softban_lock is None:
        softban_lock = asyncio.Lock()
    return softban_lock

# 请求计数器（按通道区分）- 使用字典存储
account_counters = {
    'a': 0,
    'j': 0,
    'b': 0,
    'h': 0,
    'k': 0,
    'e': 0,
    'c': 0
}
account_lock: asyncio.Lock = None  # 计数器锁

def get_account_lock():
    """获取或创建计数器锁"""
    global account_lock
    if account_lock is None:
        account_lock = asyncio.Lock()
    return account_lock

# 账号池轮询索引与锁（每个通道独立维护自己的账号索引）
account_pool_indices = {
    'a': 0,
    'j': 0,
    'b': 0,
    'h': 0,
    'k': 0,
    'e': 0,
    'c': 0
}
account_pool_lock: asyncio.Lock = None


def get_account_pool_lock():
    """获取或创建账号池锁"""
    global account_pool_lock
    if account_pool_lock is None:
        account_pool_lock = asyncio.Lock()
    return account_pool_lock


async def get_next_account(request_type: str):
    """
    从账号池中按顺序轮询取下一个账号（每个通道独立循环）
    ACCOUNT_POOL 的结构：[{ "name": ..., "mobile": "...", "token": "...", "cookies": {...} }, ...]
    
    Args:
        request_type: 请求类型（'a', 'j', 'b', 'h', 'k', 'e', 'c'）
    """
    global account_pool_indices

    if not ACCOUNT_POOL:
        raise RuntimeError("账号池为空，请在 config.ACCOUNT_POOL 中配置至少一个账号")

    async with get_account_pool_lock():
        # 获取当前通道的账号索引
        current_index = account_pool_indices.get(request_type, 0)
        account = ACCOUNT_POOL[current_index % len(ACCOUNT_POOL)]
        # 更新当前通道的账号索引（循环）
        account_pool_indices[request_type] = (current_index + 1) % len(ACCOUNT_POOL)
        return account

# 动态请求速率控制：根据是否有票调整请求频率
# 平时慢速请求，检测到有票后加快，一段时间后无新票恢复慢速
ticket_detected_time = None  # 检测到有票的时间戳
ticket_detected_lock: asyncio.Lock = None  # 有票状态锁
SLOW_INTERVAL_MIN = 20  # 慢速请求间隔（秒）- 最小值
SLOW_INTERVAL_MAX = 23  # 慢速请求间隔（秒）- 最大值
FAST_INTERVAL_MIN = 15 # 快速请求间隔（秒）- 最小值（检测到有票后）
FAST_INTERVAL_MAX = 18  # 快速请求间隔（秒）- 最大值（检测到有票后）
TICKET_TIMEOUT = 5 * 60  # 一段时间后无新票恢复慢速（秒）

def get_ticket_detected_lock():
    """获取或创建有票状态锁"""
    global ticket_detected_lock
    if ticket_detected_lock is None:
        ticket_detected_lock = asyncio.Lock()
    return ticket_detected_lock

async def mark_ticket_detected():
    """标记检测到有票"""
    global ticket_detected_time
    async with get_ticket_detected_lock():
        was_fast_mode = ticket_detected_time is not None
        ticket_detected_time = datetime.now().timestamp()
        if not was_fast_mode:
            print(f"[速率控制] 🚀 检测到有票，切换到快速请求模式（间隔 {FAST_INTERVAL_MIN}-{FAST_INTERVAL_MAX} 秒）")
        # 如果已经在快速模式，更新计时器但不打印消息（避免日志过多）

async def get_request_interval():
    """根据当前状态获取请求间隔"""
    global ticket_detected_time
    async with get_ticket_detected_lock():
        if ticket_detected_time is None:
            # 慢速模式
            return random.randint(SLOW_INTERVAL_MIN, SLOW_INTERVAL_MAX)
        else:
            # 检查是否超过30分钟
            now = datetime.now().timestamp()
            time_since_detection = now - ticket_detected_time
            if time_since_detection >= TICKET_TIMEOUT:
                # 30分钟无新票，恢复慢速
                ticket_detected_time = None
                print(f"[速率控制] 🐢 30分钟无新票，切换到慢速请求模式（间隔 {SLOW_INTERVAL_MIN}-{SLOW_INTERVAL_MAX} 秒）")
                return random.randint(SLOW_INTERVAL_MIN, SLOW_INTERVAL_MAX)
            else:
                # 快速模式
                return random.randint(FAST_INTERVAL_MIN, FAST_INTERVAL_MAX)


def get_current_pause_duration_seconds() -> int:
    """
    根据当前状态返回熔断暂停时长：
    - 认为处于放票/高峰期（最近检测到有票且未超过 TICKET_TIMEOUT）时：20 秒
    - 其他空闲时段：40 秒

    如需后期调整，可直接修改顶部的
    PAUSE_DURATION_SECONDS_ACTIVE / PAUSE_DURATION_SECONDS_IDLE 常量。
    """
    global ticket_detected_time

    # 最近有票，且仍在“有票有效期”内，认为是放票高峰期
    if ticket_detected_time is not None:
        now_ts = datetime.now().timestamp()
        if now_ts - ticket_detected_time < TICKET_TIMEOUT:
            return PAUSE_DURATION_SECONDS_ACTIVE

    # 其他情况按空闲期处理
    return PAUSE_DURATION_SECONDS_IDLE

# 代理刷新策略：同一渠道连续失败 3 次才触发刷新；刷新由后台任务合并/去重执行
FAILURES_TO_REFRESH = 2
consecutive_failures = {k: 0 for k in account_counters.keys()}
failures_lock: asyncio.Lock = None

refresh_queue: asyncio.Queue = None  # 触发刷新代理的队列（合并/去重）
refresh_in_progress = False
refresh_state_lock: asyncio.Lock = None


def get_failures_lock():
    """获取或创建失败计数锁"""
    global failures_lock
    if failures_lock is None:
        failures_lock = asyncio.Lock()
    return failures_lock


def get_refresh_queue():
    """获取或创建刷新队列（容量1，用于合并多个刷新请求）"""
    global refresh_queue
    if refresh_queue is None:
        refresh_queue = asyncio.Queue(maxsize=1)
    return refresh_queue


def get_refresh_state_lock():
    """获取或创建刷新状态锁"""
    global refresh_state_lock
    if refresh_state_lock is None:
        refresh_state_lock = asyncio.Lock()
    return refresh_state_lock


async def record_success(request_type: str):
    """记录一次成功：清空该渠道连续失败计数"""
    async with get_failures_lock():
        consecutive_failures[request_type] = 0


async def record_failure_and_maybe_trigger_refresh(request_type: str, reason: str = ""):
    """记录一次失败；若该渠道连续失败达到阈值则触发刷新请求（不阻塞）"""
    async with get_failures_lock():
        consecutive_failures[request_type] = consecutive_failures.get(request_type, 0) + 1
        fail_count = consecutive_failures[request_type]

    if fail_count >= FAILURES_TO_REFRESH:
        # 触发刷新请求：只入队一次（队列容量1，自动合并/去重）
        q = get_refresh_queue()
        try:
            q.put_nowait((request_type, fail_count, reason, datetime.now()))
        except asyncio.QueueFull:
            # 已经有待处理的刷新请求了，直接合并（忽略）
            pass


async def proxy_refresh_worker():
    """后台任务：合并/去重地执行代理刷新"""
    global refresh_in_progress
    q = get_refresh_queue()
    while True:
        request_type, fail_count, reason, ts = await q.get()

        # drain：合并队列里可能积累的触发（容量1通常无需，但保留以防未来调整）
        while True:
            try:
                _ = q.get_nowait()
                q.task_done()
            except asyncio.QueueEmpty:
                break

        async with get_refresh_state_lock():
            if refresh_in_progress:
                q.task_done()
                continue
            refresh_in_progress = True

        try:
            reason_str = f"，原因: {reason}" if reason else ""
            print(
                f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] [PROXY] 触发刷新（渠道 {request_type} 连续失败 {fail_count} 次{reason_str}）"
            )
            await force_refresh_proxy()

            # 刷新成功后：将所有渠道的连续失败清零（避免旧失败导致立刻再次触发）
            async with get_failures_lock():
                for k in consecutive_failures.keys():
                    consecutive_failures[k] = 0
        except Exception as e:
            print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] [PROXY] 刷新代理失败: {e}")
        finally:
            async with get_refresh_state_lock():
                refresh_in_progress = False
            q.task_done()

# 统计功能：每天每个sku的放票数量
daily_stats = {}  # {sku: count}
current_date = datetime.now().date()  # 当前日期
stats_lock: asyncio.Lock = None  # 统计锁

def get_stats_lock():
    """获取或创建统计锁"""
    global stats_lock
    if stats_lock is None:
        stats_lock = asyncio.Lock()
    return stats_lock

async def reset_daily_stats():
    """重置每日统计"""
    global daily_stats, current_date
    async with get_stats_lock():
        daily_stats = {}
        current_date = datetime.now().date()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 每日统计已重置")

async def update_daily_stats(price_names):
    """更新每日统计"""
    global daily_stats, current_date
    now = datetime.now()
    today = now.date()
    
    async with get_stats_lock():
        # 如果日期变化，重置统计
        if today != current_date:
            daily_stats = {}
            current_date = today
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 每日统计已重置（日期变化）")
        
        # 更新统计
        for price_name in price_names:
            daily_stats[price_name] = daily_stats.get(price_name, 0) + 1

async def get_stats_message():
    """获取统计信息文本"""
    async with get_stats_lock():
        if not daily_stats:
            return "📊 今日统计：暂无数据"
        
        stats_lines = ["📊 今日统计："]
        for sku, count in sorted(daily_stats.items()):
            stats_lines.append(f"  {sku}: {count}次")
        return "\n".join(stats_lines)


async def send_bark_message(message: str):
    """
    发送 Bark 通知
    message 会放在 BARK_BASE_URL 最后一个斜杠后面，例如 .../start, .../stop, .../账号名
    """
    bark_url = f"{BARK_BASE_URL}/{message}"
    try:
        async with AsyncSession() as bark_session:
            await bark_session.get(bark_url, timeout=10)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 已发送 Bark 通知: {message}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 发送 Bark 通知失败({message}): {e}")

# 发送钉钉通知（异步版本，不阻塞主循环）
async def send_dingdingbot_async(tickets_info):
    """异步发送合并后的有票信息到钉钉，不阻塞主循环"""
    # 组装消息体 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"{tickets_info} \n有票通知\n⏰ {timestamp}\n\n"
    
    message = {
        "msgtype": "text",  # 消息类型
        "text": {
            "content": content
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # 使用异步会话发送请求（不阻塞主循环）
    try:
        async with AsyncSession() as notify_session:
            # 并发发送到3个钉钉机器人
            tasks = [
                notify_session.post(webhook_url, json=message, headers=headers, timeout=10),
                notify_session.post(webhook_url2, json=message, headers=headers, timeout=10),
                notify_session.post(webhook_url3, json=message, headers=headers, timeout=10),
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 检查结果（快速处理，不阻塞）
            for i, result in enumerate(results, 1):
                if isinstance(result, Exception):
                    print(f"✗ 钉钉通知{i}发送异常: {result}")
                elif result.status_code == 200:
                    print(f"✓ 钉钉通知{i}发送成功!")
                else:
                    print(f"✗ 钉钉通知{i}发送失败，状态码: {result.status_code}")
    except Exception as e:
        print(f"发送钉钉消息时发生错误: {e}")


async def pause_all_requests_due_to_softban():
    """
    触发熔断：暂停所有请求一段时间，然后自动恢复。
    会发送 Bark 通知：stop（开始暂停）和 start（恢复）。
    """
    global is_running, pause_in_progress, softban_bark_count, softban_active

    # 防止重复进入，同时标记软封禁生效
    async with get_softban_lock():
        if pause_in_progress:
            return
        pause_in_progress = True
        softban_active = True

    try:
        # 先暂停：设置全局运行标志为 False
        async with get_running_lock():
            if not is_running:
                # 已经是暂停状态，仅确保软封禁标志生效
                async with get_softban_lock():
                    pause_in_progress = False
                return
            is_running = False

        # 根据当前状态（是否最近检测到有票）动态选择熔断暂停时间
        pause_seconds = get_current_pause_duration_seconds()

        # 发送 Bark 通知：程序停止（soft stop）
        await send_bark_message("stop")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 软封禁熔断触发：暂停所有请求 {pause_seconds} 秒")

        # 暂停指定时间
        await asyncio.sleep(pause_seconds)

        # 熔断结束：根据时间窗口决定是否恢复运行
        async with get_running_lock():
            is_running = is_within_running_window()

        # 重置软封禁计数和标志
        async with get_softban_lock():
            softban_bark_count = 0
            softban_active = False

        # 发送 Bark 通知：程序重新启动（仅在当前时间允许运行时发送）
        if is_running:
            await send_bark_message("start")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 软封禁熔断结束：恢复所有请求")
    finally:
        # 无论成功与否，都要重置 pause_in_progress 状态
        async with get_softban_lock():
            pause_in_progress = False


# 发送每日统计消息到钉钉
async def send_daily_stats_to_dingding():       
    """发送每日统计消息到钉钉"""
    stats_info = await get_stats_message()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"📊 每日有票统计报告\n⏰ {timestamp}\n\n{stats_info}"
    
    message = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # 发送POST请求到钉钉机器人接口
    try:
        response = requests.post(webhook_url, data=json.dumps(message), headers=headers)
        response2 = requests.post(webhook_url2, data=json.dumps(message), headers=headers)
        response3 = requests.post(webhook_url3, data=json.dumps(message), headers=headers)

        if response.status_code == 200:
            print("✓ 每日统计消息1发送成功!")
        else:
            print(f"✗ 每日统计消息1发送失败，状态码: {response.status_code}, 错误信息: {response.text}")
        
        if response2.status_code == 200:
            print("✓ 每日统计消息2发送成功!")
        else:
            print(f"✗ 每日统计消息2发送失败，状态码: {response2.status_code}, 错误信息: {response2.text}")

        if response3.status_code == 200:
            print("✓ 每日统计消息3发送成功!")
        else:
            print(f"✗ 每日统计消息3发送失败，状态码: {response3.status_code}, 错误信息: {response3.text}")
    except Exception as e:
        print(f"发送每日统计消息时发生错误: {e}")


# 请求
async def async_post_request(session, url, request_type):
    global is_running, account_counters
    while True:
        # 检查运行状态（快速检查，不获取锁）
        if not is_running:
            # 使用短间隔检查，避免长时间占用资源
            await asyncio.sleep(5)  # 暂停时每5秒检查一次，响应更快
            continue
        try:
            # 从账号池中取出当前要使用的账号（每个通道独立循环）
            account = await get_next_account(request_type)
            
            # 复制 headers 模板，并动态更新 fullmobile 和 token
            request_headers = headers.copy()
            request_headers["fullmobile"] = account["mobile"]
            request_headers["token"] = account["token"]
            cookies = account.get("cookies", {})

            # 获取当前代理配置
            proxy_dict = await get_proxy_dict()
            # curl_cffi 使用字符串格式的代理URL
            proxy_url = proxy_dict.get("http") if proxy_dict else None
            
            # 使用 curl_cffi 的异步请求
            response = await session.get(
                url, 
                headers=request_headers, 
                cookies=cookies,
                proxy=proxy_url,
                timeout=30
            )
            
            if response.status_code == 200:
                await record_success(request_type)
                # 更新对应渠道的计数器（使用锁保证线程安全）
                async with get_account_lock():
                    account_counters[request_type] += 1
                    current_count = account_counters[request_type]

                print(f'{request_type} 请求了 {current_count} 次，使用账号: {account.get("name", account.get("mobile", "unknown"))}')
                

                # curl_cffi 的响应对象，text 是属性不是方法
                data = response.text
                print(f"请求成功！返回数据：{datetime.now().strftime('%m-%d %H:%M:%S')}")
                data1 = json.loads(data)
                showSessionModelList = data1.get('data', {}).get('showSessionModelList', [])
                # print(showSessionModelList)
                # 如果 showSessionModelList 为空，意味着账号被封/软封禁，发送 Bark 通知
                if not showSessionModelList:
                    try:
                        # 获取账号名称（优先使用 name，否则使用 mobile）
                        account_name = account.get("name", account.get("mobile", "unknown"))
                        # 发送 Bark 通知：账号名作为 message 放到 URL 最后一段
                        await send_bark_message(account_name)
                        print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] 检测到账号被封/软封禁: {account_name}，已发送 Bark 通知")

                        # 累计软封禁 Bark 次数，达到阈值后触发全局熔断暂停
                        global softban_bark_count
                        async with get_softban_lock():
                            softban_bark_count += 1
                            current_softban_count = softban_bark_count

                        if current_softban_count >= SOFTBAN_BARK_THRESHOLD:
                            print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] 软封禁 Bark 次数达到阈值 {SOFTBAN_BARK_THRESHOLD}，触发熔断暂停")
                            # 在后台异步执行暂停流程，避免阻塞当前请求协程
                            asyncio.create_task(pause_all_requests_due_to_softban())

                    except Exception as e:
                        print(f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] 发送 Bark 通知失败: {e}")

                # 收集本次请求中所有“有票”的 priceName
                # 判断条件：stock > 0 即认为有票（仅用于判断，不在打印/钉钉消息中展示库存）
                available_ticket_names = [
                    priceInfoMode["priceName"].split("/", 1)[0].strip()
                    for session_item in showSessionModelList
                    for priceInfoMode in session_item.get("priceInfoModelList", [])
                    if priceInfoMode.get("stock", 0) > 0
                ]
                
                # 如果有票，批量打印并异步处理通知（不阻塞主循环）
                if available_ticket_names:
                    # 标记检测到有票，切换到快速请求模式
                    await mark_ticket_detected()

                    # 批量打印所有有票信息（不包含库存）
                    print(f"[{request_type}] 检测到有票: {', '.join(available_ticket_names)}")

                    # 用制表位（Tab）分隔所有有票信息（不包含库存）
                    tickets_info = "\t".join(available_ticket_names)
                    
                    # 将统计更新和通知发送放到后台任务，不阻塞主循环
                    # 使用 create_task 让这些操作在后台异步执行，主循环可以继续请求
                    asyncio.create_task(update_daily_stats(available_ticket_names))
                    asyncio.create_task(send_dingdingbot_async(tickets_info))
            else:
                print(f"请求失败，状态码：{response.status_code}")
                await record_failure_and_maybe_trigger_refresh(
                    request_type, reason=f"HTTP {response.status_code}"
                )

            # 使用动态请求间隔：根据是否有票调整请求频率
            wait_time = await get_request_interval()
            await asyncio.sleep(wait_time)
        except Exception as e:
            # curl_cffi 的异常处理（统一处理所有异常）
            error_msg = str(e)
            print(f"{request_type} 请求错误：{error_msg}")
            await record_failure_and_maybe_trigger_refresh(request_type, reason=error_msg)
            # 失败后使用较短的等待时间，但仍遵循动态速率控制
            wait_time = await get_request_interval()
            # 失败后等待时间减半，但最少2秒
            wait_time = max(2, wait_time // 2)
            await asyncio.sleep(wait_time)


# 定时控制任务
async def schedule_controller():
    """
    定时控制任务：每天0点关闭，7点启动，并在新的一天重置统计
    每天22点发送每日统计消息
    """
    global is_running, current_date, daily_stats, softban_active
    
    # 初始化运行状态和统计
    async with get_running_lock():
        # 初始时根据时间窗口和软封禁状态决定是否运行
        is_running = is_within_running_window() and not softban_active
        if is_running:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序启动：当前时间在运行时段内")
            # 每天程序首次启动时发送 Bark 通知（start）
            await send_bark_message("start")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序暂停：等待早上启动")
    
    # 初始化统计（在事件循环中调用）
    await reset_daily_stats()
    
    # 记录上次发送统计消息的日期，避免同一天重复发送
    last_stats_sent_date = None
    
    while True:
        try:
            now = datetime.now()
            today = now.date()
            current_time = now.time()
            # 只有在时间窗口内且未处于软封禁期才“应该运行”
            should_run = is_within_running_window(now) and not softban_active
            
            # 如果程序未运行，计算到启动时间的精确等待时间
            if not is_running and should_run:
                # 直接启动，不等待
                async with get_running_lock():
                    if not is_running and not softban_active:  # 双重检查并避开熔断期
                        is_running = True
                        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] ✅ 程序启动：开始发送请求和更新代理")
                        # 每天运行时段开始时发送 Bark 通知（start）
                        await send_bark_message("start")
            elif not is_running and not should_run:
                # 计算到启动时间的精确秒数
                current_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
                start_seconds = START_TIME.hour * 3600 + START_TIME.minute * 60 + START_TIME.second
                
                # 计算需要等待的秒数
                if current_seconds < start_seconds:
                    seconds_until_start = start_seconds - current_seconds
                    # 如果距离启动时间超过5分钟，使用较长的等待时间（但不超过60秒）
                    if seconds_until_start > 300:
                        wait_time = min(60, seconds_until_start - 300)
                    # 如果距离启动时间在1-5分钟之间，使用10秒等待
                    elif seconds_until_start > 60:
                        wait_time = min(10, seconds_until_start - 60)
                    # 如果距离启动时间在1分钟内，精确等待到启动时间
                    else:
                        wait_time = seconds_until_start
                    
                    await asyncio.sleep(wait_time)
                    continue  # 继续循环，立即检查是否应该启动
                else:
                    # 当前时间已过启动时间，但程序未运行，立即检查
                    await asyncio.sleep(1)
                    continue
            
            # 检查日期变化，重置统计（避免死锁：直接在锁内重置，不调用函数）
            async with get_stats_lock():
                if today != current_date:
                    daily_stats = {}
                    current_date = today
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 每日统计已重置（日期变化）")
                    last_stats_sent_date = None  # 重置统计发送日期
            
            # 检查是否到了统计消息发送时间，发送每日统计消息
            if current_time.hour == STATS_TIME.hour and current_time.minute == STATS_TIME.minute:
                if last_stats_sent_date != today:
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 📊 开始发送每日统计消息...")
                    await send_daily_stats_to_dingding()
                    last_stats_sent_date = today
            
            # 检查是否需要停止
            if not should_run and is_running:
                async with get_running_lock():
                    if is_running:  # 双重检查
                        is_running = False
                        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] ⏸️ 程序暂停：停止发送请求和更新代理")
                        # 每天运行时段结束时发送 Bark 通知（stop）
                        await send_bark_message("stop")
            
            # 程序运行中，每分钟检查一次即可
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"定时控制任务错误: {e}")
            await asyncio.sleep(10)


# 主函数
async def main():
    global is_running
    
    # 显示初始请求速率模式
    print(f"[速率控制] 🐢 初始模式：慢速请求（间隔 {SLOW_INTERVAL_MIN}-{SLOW_INTERVAL_MAX} 秒）")
    print(f"[速率控制] 📋 检测到有票后将切换到快速模式（间隔 {FAST_INTERVAL_MIN}-{FAST_INTERVAL_MAX} 秒）")
    print(f"[速率控制] ⏰ 30分钟无新票后自动恢复慢速模式")
    
    # 启动定时控制任务
    schedule_task = asyncio.create_task(schedule_controller())
    
    # 等待一下，让定时控制器初始化
    await asyncio.sleep(1)
    
    # 启动代理更新后台任务（传入运行状态检查函数）
    def get_running_status():
        return is_running
    
    proxy_task = asyncio.create_task(proxy_updater_task(get_running_status))
    # 启动代理刷新后台任务：合并/去重执行 force_refresh_proxy()
    refresh_worker_task = asyncio.create_task(proxy_refresh_worker())
    
    # 使用 curl_cffi 的异步会话，添加浏览器指纹模拟
    # 可选值: chrome99, chrome100, chrome101, chrome104, chrome107, chrome110, chrome116, chrome119, chrome120, chrome123, edge99, edge101, safari15_3, safari15_5
    # 启动前先检查账号池是否为空
    if not ACCOUNT_POOL:
        print("账号池为空，请在 config.ACCOUNT_POOL 中配置至少一个账号")
        return

    async with AsyncSession(impersonate="chrome123") as session:
        tasks = [
            async_post_request(session, url_a, 'a'),
            async_post_request(session, url_j, 'j'),
            async_post_request(session, url_b, 'b'),
            async_post_request(session, url_h, 'h'),
            async_post_request(session, url_k, 'k'),
            async_post_request(session, url_e, 'e'),
            async_post_request(session, url_c, 'c'),
        ]
        await asyncio.gather(*tasks, proxy_task, schedule_task, refresh_worker_task)


if __name__ == '__main__':
    asyncio.run(main())


