import asyncio
from curl_cffi.requests import AsyncSession

url = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931332204da960001241231&sign=RTJGQTY1QkY5N0Q0NUM1MzM4RkEwNDk0Q0I5MjcxMTk%3D"
cookies = {
  "ssxmod_itna3": "C50qzxRD0Duj0=GCWDCD27jNG=2YGKPG87ekiQWDCxrPqGXHGFjzx8qY=G2DmqB=DugqGODAM9Us4=/40aBDBKDRl=DYDijAB3h=sz=Y3aL2Clix3KU/B3KDZDGKGXDQeDvz29+f=f/jgPD7q5DtqU+RYNd/Sx3WirK1lpPz24rz2DYwE25V72HBQu8K6Rbo=IHeD",
}

headers = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "18942240295",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "m9/3qR2DKWt3+Xm+MvfUR1ORq14j0JiN2n/U/viDQftEJIdMSbVPsmsD/uWPLfQYbQrUONwK89UhSWlx4twH4vZLaZjnol62Sr4vFvL0X1/tBCRNBafHYKd2KWrR83n/OhzusSAlEbWcJev1fRUCmJ052mGIsGj3z7wz2iMePh8",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}


async def test_request():
    """异步测试请求函数"""
    # 使用 curl_cffi 的异步会话，添加 impersonate 参数模拟浏览器指纹
    # 可选值: chrome99, chrome100, chrome101, chrome104, chrome107, chrome110, chrome116, chrome119, chrome120, chrome123, edge99, edge101, safari15_3, safari15_5
    # 由于 User-Agent 是 Chrome 132，选择 chrome123 作为最接近的版本
    async with AsyncSession(impersonate="chrome123") as session:
        try:
            res = await session.get(url, headers=headers, cookies=cookies, timeout=30)
            print(f"状态码: {res.status_code}")
            print(f"响应内容:\n{res.text}")
            return res
        except Exception as e:
            print(f"请求错误: {e}")
            return None


if __name__ == "__main__":
    # 运行异步函数
    asyncio.run(test_request())
