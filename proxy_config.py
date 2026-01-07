"""
代理IP配置文件
用于获取和管理代理IP，每55秒自动更新
"""
import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Optional, Tuple

# 代理IP获取接口（需要替换为实际接口地址）
PROXY_API_URL = "https://share.proxy.qg.net/get?key=BCAA9684&distinct=true"  # 请替换为实际的代理IP接口地址

# 代理认证信息
PROXY_USERNAME = "BCAA9684"
PROXY_PASSWORD = "37235174D5F3"

# 当前代理信息
_current_proxy: Optional[Tuple[str, int]] = None
_last_update_time: Optional[datetime] = None
_update_lock: Optional[asyncio.Lock] = None


def _get_lock() -> asyncio.Lock:
    """获取或创建锁对象"""
    global _update_lock
    if _update_lock is None:
        _update_lock = asyncio.Lock()
    return _update_lock


async def fetch_proxy_ip() -> Optional[Tuple[str, int]]:
    """
    从接口获取代理IP和端口
    返回: (ip, port) 或 None
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(PROXY_API_URL, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # 解析返回的JSON数据
                    if data.get("code") == "SUCCESS" and data.get("data"):
                        proxy_data = data["data"][0]  # 取第一个代理
                        server = proxy_data.get("server", "")
                        
                        if server:
                            # server格式: "120.220.19.212:20021"
                            parts = server.split(":")
                            if len(parts) == 2:
                                ip = parts[0]
                                port = int(parts[1])
                                print(f"✓ 获取到代理IP: {ip}:{port}")
                                return (ip, port)
                            else:
                                print(f"✗ 代理IP格式错误: {server}")
                        else:
                            print("✗ 返回数据中没有server字段")
                    else:
                        print(f"✗ 接口返回错误: {data.get('code', 'UNKNOWN')}")
                else:
                    print(f"✗ 获取代理IP失败，状态码: {response.status}")
    except Exception as e:
        print(f"✗ 获取代理IP时发生错误: {e}")
    
    return None


async def get_proxy(force_refresh: bool = False) -> Optional[str]:
    """
    获取当前可用的代理URL（带认证）
    返回格式: http://username:password@ip:port
    
    Args:
        force_refresh: 是否强制刷新代理（忽略时间间隔）
    """
    global _current_proxy, _last_update_time
    
    async with _get_lock():
        # 检查是否需要更新代理（每55秒更新一次）
        now = datetime.now()
        need_update = force_refresh or _current_proxy is None or _last_update_time is None or \
           (now - _last_update_time).total_seconds() >= 58
        
        if need_update:
            print(f"[{now.strftime('%H:%M:%S')}] 正在更新代理IP...")
            new_proxy = await fetch_proxy_ip()
            if new_proxy:
                _current_proxy = new_proxy
                _last_update_time = now
            elif _current_proxy is None:
                # 如果获取失败且没有旧代理，返回None
                return None
        
        if _current_proxy:
            ip, port = _current_proxy
            # 构建带认证的代理URL
            proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{ip}:{port}"
            return proxy_url
    
    return None


async def force_refresh_proxy() -> Optional[str]:
    """
    强制刷新代理IP（忽略时间间隔）
    用于请求失败时立即获取新代理
    """
    return await get_proxy(force_refresh=True)


async def get_proxy_dict(force_refresh: bool = False) -> Optional[dict]:
    """
    获取aiohttp使用的代理字典格式
    返回: {"http": "http://username:password@ip:port"} 或 None
    
    Args:
        force_refresh: 是否强制刷新代理
    """
    proxy_url = await get_proxy(force_refresh=force_refresh)
    if proxy_url:
        return {"http": proxy_url, "https": proxy_url}
    return None


# 后台任务：定期更新代理IP
async def proxy_updater_task(is_running_flag):
    """
    后台任务，每55秒更新一次代理IP
    
    Args:
        is_running_flag: 运行状态标志的getter函数
    """
    # 启动时立即获取一次代理
    print("正在初始化代理IP...")
    await get_proxy()
    
    while True:
        try:
            # 检查运行状态
            if not is_running_flag():
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 代理更新已暂停")
                await asyncio.sleep(60)  # 暂停时每分钟检查一次
                continue
            
            await asyncio.sleep(58)  # 等待55秒
            await get_proxy()  # 更新代理
        except Exception as e:
            print(f"代理更新任务错误: {e}")
            await asyncio.sleep(10)  # 出错后等待10秒再重试
