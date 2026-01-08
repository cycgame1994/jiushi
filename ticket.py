import random
import json
from datetime import datetime, time as dt_time
import aiohttp
import asyncio
import requests
from config import (
    url,
    webhook_url,
    webhook_url2,
    webhook_url3,
    headersa,
    headersj,
    headersd,
    headersb,
    headersh,
    headersk,
    headerse,
    headersc,
    paramsa,
    paramsj,
    paramsd,
    paramsb,
    paramsh,
    paramsk,
    paramse,
    paramsc,
)
from proxy_config import get_proxy_dict, proxy_updater_task, force_refresh_proxy

"""
1.增加代理ip,轮询请求网址 √
2.增加每天定时启动，关闭发送请求 √
3.监控到有票后，增加请求频率，平时请求间隔大。
4.增加统计功能，监控到有票后，统计每一种票的库存数量，发送到钉钉消息
5.失败重试机制，每5次失败发送推送消息到ios的bark
6.按照a,j,d,b,h,k,e,c的顺序请求，每一轮发送钉钉消息，而不是每一次请求发一次，并且消息中带有时间戳
7，为后续和手机的autox自动抢票做准备，检测到有票后，发送websocket信息给手机的autox
"""
# 运行状态控制
is_running = False  # 全局运行标志
running_lock: asyncio.Lock = None  # 运行状态锁


def get_running_lock():
    """获取或创建运行状态锁"""
    global running_lock
    if running_lock is None:
        running_lock = asyncio.Lock()
    return running_lock

# 请求计数器（按通道区分）
account_a = 0
account_j = 0
account_d = 0
account_b = 0
account_h = 0
account_k = 0
account_e = 0
account_c = 0

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

# 发送钉钉通知
def send_dingdingbot(tickets_info, stats_info=""):
    """发送合并后的有票信息到钉钉"""
    # 组装消息体
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"🎫 有票通知\n⏰ {timestamp}\n\n{tickets_info}"
    # if stats_info:
    #     content += f"\n\n{stats_info}"
    
    message = {
        "msgtype": "text",  # 消息类型
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
            print("✓ 钉钉通知1发送成功!")
        else:
            print(f"✗ 钉钉通知1发送失败，状态码: {response.status_code}, 错误信息: {response.text}")
        
        if response2.status_code == 200:
            print("✓ 钉钉通知2发送成功!")
        else:
            print(f"✗ 钉钉通知2发送失败，状态码: {response2.status_code}, 错误信息: {response2.text}")

        if response3.status_code == 200:
            print("✓ 钉钉通知3发送成功!")
        else:
            print(f"✗ 钉钉通知3发送失败，状态码: {response3.status_code}, 错误信息: {response3.text}")
    except Exception as e:
        print(f"发送钉钉消息时发生错误: {e}")


# 请求
async def async_post_request(session, headers, params, account_counter):
    global is_running
    while True:
        # 检查运行状态（先快速检查，避免频繁获取锁）
        if not is_running:
            async with get_running_lock():
                # 再次确认状态（双重检查）
                if not is_running:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 程序已暂停，等待启动时间...")
                    await asyncio.sleep(60)  # 暂停时每分钟检查一次
                    continue
        try:
            # 获取当前代理配置
            proxy_dict = await get_proxy_dict()
            # 使用代理发送请求（如果代理可用）
            proxy_url = proxy_dict.get("http") if proxy_dict else None
            async with session.get(url, headers=headers, params=params, proxy=proxy_url, ssl=False) as response:
                if response.status == 200:
                    account_counter += 1
                    # request_type = 'b' if headers == headersb else 'k'
                    if headers == headersa:
                        request_type = 'a'
                    elif headers == headersj:
                        request_type = 'j'
                    elif headers == headersd:
                        request_type = 'd'
                    elif headers == headersb:
                        request_type = 'b'
                    elif headers == headersh:
                        request_type = 'h'
                    elif headers == headersk:
                        request_type = 'k'
                    elif headers == headerse:
                        request_type = 'e'
                    elif headers == headersc:
                        request_type = 'c'
                    else:
                        request_type = '?'

                    print(f'{request_type}请求了{account_counter}次')

                    data = await response.text()
                    print("请求成功！返回数据：", datetime.now().strftime("%m-%d %H:%M:%S"))
                    data1 = json.loads(data)
                    showSessionModelList = data1['data']['showSessionModelList']
                    
                    # 收集本次请求中所有有库存的priceName
                    available_tickets = []
                    for i in range(len(showSessionModelList)):
                        priceInfoModelList = showSessionModelList[i]['priceInfoModelList']
                        for priceInfoMode in priceInfoModelList:
                            if priceInfoMode['stock'] == 1:
                                # 去掉价格后面的/及其后内容，仅保留斜杠前部分
                                priceName = priceInfoMode['priceName'].split('/', 1)[0].strip()
                                available_tickets.append(priceName)
                                print(priceName)
                    
                    # 如果有库存，合并发送消息并更新统计
                    if available_tickets:
                        # 用制表位（Tab）分隔所有有票信息
                        tickets_info = "\t".join(available_tickets)
                        
                        # 更新每日统计
                        await update_daily_stats(available_tickets)
                        
                        # 获取统计信息
                        stats_info = await get_stats_message()
                        
                        # 发送合并后的消息
                        send_dingdingbot(tickets_info, stats_info)
                else:
                    print(f"请求失败，状态码：{response.status}")
                    # 请求失败时强制刷新代理
                    print("请求失败，正在重新获取代理IP...")
                    await force_refresh_proxy()

            await asyncio.sleep(random.randint(5, 8))
            # time.sleep(random.randint(1, 5))
        except aiohttp.ClientError as e:
            # 代理相关错误（408超时、502、503等）
            error_msg = str(e)
            print(f"代理请求错误：{error_msg}")
            # 强制刷新代理
            print("检测到代理错误，正在重新获取代理IP...")
            await force_refresh_proxy()
            await asyncio.sleep(random.randint(2, 4))
        except Exception as e:
            print(f"发生错误：{e}")
            # 其他错误也尝试刷新代理
            await force_refresh_proxy()
            await asyncio.sleep(random.randint(1, 5))


# 定时控制任务
async def schedule_controller():
    """
    定时控制任务：每天0点关闭，6点启动，并在新的一天重置统计
    """
    global is_running, current_date
    
    def should_be_running():
        """判断当前时间是否应该在运行
        运行时间：早上8:00:00 到 晚上23:00:00
        关闭时间：凌晨0:00:00 到 早上7:59:59
        """
        now = datetime.now()
        current_time = now.time()
        start_time = dt_time(9, 34, 0)   # 8:00:00
        end_time = dt_time(23, 00, 00)  # 23:00:00

        # 8点到23:00:00之间运行 0点到7:59:59之间关闭
        return start_time <= current_time <= end_time
    
    # 初始化运行状态和统计
    async with get_running_lock():
        is_running = should_be_running()
        if is_running:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序启动：当前时间在运行时段内")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序暂停：等待早上8点启动")
    
    # 初始化统计（在事件循环中调用）
    await reset_daily_stats()
    
    while True:
        try:
            await asyncio.sleep(60)  # 每分钟检查一次
            
            now = datetime.now()
            today = now.date()
            current_time = now.time()
            should_run = should_be_running()
            
            # 检查日期变化，重置统计
            async with get_stats_lock():
                if today != current_date:
                    await reset_daily_stats()
            
            async with get_running_lock():
                if should_run and not is_running:
                    # 启动
                    is_running = True
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] ✅ 程序启动：开始发送请求和更新代理")
                elif not should_run and is_running:
                    # 关闭
                    is_running = False
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] ⏸️ 程序暂停：停止发送请求和更新代理")
        except Exception as e:
            print(f"定时控制任务错误: {e}")
            await asyncio.sleep(10)


# 主函数
async def main():
    global is_running
    
    # 启动定时控制任务
    schedule_task = asyncio.create_task(schedule_controller())
    
    # 等待一下，让定时控制器初始化
    await asyncio.sleep(1)
    
    # 启动代理更新后台任务（传入运行状态检查函数）
    def get_running_status():
        return is_running
    
    proxy_task = asyncio.create_task(proxy_updater_task(get_running_status))
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            async_post_request(session, headersa, paramsa, account_a),
            async_post_request(session, headersj, paramsj, account_j),
            async_post_request(session, headersd, paramsd, account_d),
            async_post_request(session, headersb, paramsb, account_b),
            async_post_request(session, headersh, paramsh, account_h),
            async_post_request(session, headersk, paramsk, account_k),
            async_post_request(session, headerse, paramse, account_e),
            async_post_request(session, headersc, paramsc, account_c),
        ]
        await asyncio.gather(*tasks, proxy_task, schedule_task)


if __name__ == '__main__':
    asyncio.run(main())

