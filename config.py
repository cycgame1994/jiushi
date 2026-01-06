import random
import base64
import urllib.parse

# 原始 sign 值
raw_signa = "RTJGQTY1QkY5N0Q0NUM1MzM4RkEwNDk0Q0I5MjcxMTk%3D"
raw_signj = "QTU4RDhGQzkwQUVFNUYzRDMyMzc5MjQ1NTQ3NjNDM0I%3D"
raw_signd = "RTUwMTJEOUI3MTRGOUI0NzEwNzRBQzI4ODFBMzQzQTg%3D"
raw_signb = "N0M1MDBBMTBDQkNCOEM4Njk1REVBMDVDNTU4ODQxMTM%3D"
raw_signh = "MzBCMTNDRjdFNTBDQjdDOTEwREExM0NGQTZCM0MwMzc%3D"
raw_signk = "RUI0N0ZDNUU1QjgzNzBEMTY3QzQyRUM5QjQ4QkMyMzk%3D"
raw_signe = "MUU2NkIxNkNGNjA5NDg4NTg2RENFQTJEQjE3NjRBMzY%3D"
raw_signc = "NjVDMTNFRDY2MTU0NUU0QUUzQTlGM0U3MTZDMzlCOTg%3D"


def parseSign(raw_sign: str) -> str:
    """解析 sign 值，如果不是合法 Base64 则重新编码"""
    decoded_sign = urllib.parse.unquote(raw_sign)
    try:
        base64.b64decode(decoded_sign)
    except Exception:
        return base64.b64encode(decoded_sign.encode("utf-8")).decode("utf-8")
    return decoded_sign


# 用户代理列表
user_agent_list = [
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
]


# URL
url = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew"
# 钉钉通知地址
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=bdc3b8bd0e3ebdb39df90bf67acbbf405d04b60065db1dfe37c6c8e938f52221"
webhook_url2 = "https://oapi.dingtalk.com/robot/send?access_token=40442c548b938e2cd769e462a4f2a0a69cf9482a2deb299a154f3a1bea45c48a"
webhook_url3 = "https://oapi.dingtalk.com/robot/send?access_token=61cb96708c2543536319fff172477490cfc3cccb703fa73a0d168786928054f8"


# 参数头部
headersa = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/124/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersj = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersd = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersb = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxRDgAYew4WweQw2xUx7TeiTeDIYfK5diDHii1QDBuPAP5HG9Dbq7QDgDzq7UzDQqD19ngd7rHDUSKDyDiFXxVDD+qiFoAEwLxivFPKPe7Dh0DPFLDxqGzDiq0HDK4GTUS04aeazxG6kDBjBYS4ZC0dQDD5ySirH8n=eCuhYCgPYZbb5TCr5shIr1hWbh2PxD",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersh = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/124/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersk = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headerse = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxRDgAYew4WweQw2xUx7TeiTeDIYfK5diDHii1QDBuPAP5HG9Dbq7QDgDzq7UzDQqD19ngd7rHDUSKDyDiFXxVDD+qiFoAEwLxivFPKPe7Dh0DPFLDxqGzDiq0HDK4GTUS04aeazxG6kDBjBYS4ZC0dQDD5ySirH8n=eCuhYCgPYZbb5TCr5shIr1hWbh2PxD",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

headersc = {
    "Host": "jsapp.jussyun.com",
    "Connection": "keep-alive",
    "os_type": "wechat_mini",
    "fullMobile": "[object Undefined]",
    "app_id": "7134142a2721aa804af172b5c1d55e0c",
    "os_version": "Windows 10 x64",
    "User-Agent": random.choice(user_agent_list),
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "cookie": "ssxmod_itna3=C50qzxuDBD9DR0D2DUEfQWKAKD=C6qHmbwxDQDUBGKOD0vdidrUD6xmK07DRxlK0CZD7KDSjEuH0+UDCc=DUxGjzq/xDmYIjbGx5HqGt63QetI7Rr4FLQxqGzDiq0HDK4GTUB04pKazx09=DCKCehrzrBce3nIY3RAdtnFe8BRdt4u+=IAd8/4=GSbAh4wd4D",
    "device_type": "microsoft",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/125/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


# 请求参数
paramsa = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "6931332204da960001241231",
    "sign": parseSign(raw_signa),
}

paramsj = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "6931340149963100012455d5",
    "sign": parseSign(raw_signj),
}

paramsd = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "6932f256499631000135691a",
    "sign": parseSign(raw_signd),
}

paramsb = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "693132e14996310001244821",
    "sign": parseSign(raw_signb),
}

paramsh = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "69315292499631000125952f",
    "sign": parseSign(raw_signh),
}

paramsk = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "693152ad4996310001259691",
    "sign": parseSign(raw_signk),
}

paramse = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "693152c604da960001255ee6",
    "sign": parseSign(raw_signe),
}

paramsc = {
    "inWhite": "false",
    "os_type": "wechat_mini",
    "showId": "6931535304da960001256176",
    "sign": parseSign(raw_signc),
}

