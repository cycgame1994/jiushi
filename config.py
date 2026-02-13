import random
import base64
import urllib.parse




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
url_a = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931332204da960001241231&sign=RTJGQTY1QkY5N0Q0NUM1MzM4RkEwNDk0Q0I5MjcxMTk%3D"
url_j = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931340149963100012455d5&sign=QTU4RDhGQzkwQUVFNUYzRDMyMzc5MjQ1NTQ3NjNDM0I%3D"# 钉钉通知地址
url_b = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693132e14996310001244821&sign=N0M1MDBBMTBDQkNCOEM4Njk1REVBMDVDNTU4ODQxMTM%3D"
url_h = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=69315292499631000125952f&sign=MzBCMTNDRjdFNTBDQjdDOTEwREExM0NGQTZCM0MwMzc%3D"
url_k = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693152ad4996310001259691&sign=RUI0N0ZDNUU1QjgzNzBEMTY3QzQyRUM5QjQ4QkMyMzk%3D"
url_e = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693152c604da960001255ee6&sign=MUU2NkIxNkNGNjA5NDg4NTg2RENFQTJEQjE3NjRBMzY%3D"
url_c = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931535304da960001256176&sign=NjVDMTNFRDY2MTU0NUU0QUUzQTlGM0U3MTZDMzlCOTg%3D"

# cookies
cookies= {
  "ssxmod_itna3": "C50qzxRDuDyDgDGxhDcAGKiQQG=t5D=t3WCCGCKiDUGjIOD0HQidO2D6xmK07DRxB=DuxeGODAdHXGerKq0aSDBKDRDtiYDiRDodhT2KQc39O3i0i+xPXDZ8KDZDGKGXDQeDv+gtu3tLioKD7T5DtTUwn7XQDoKKDD5YFjrYpexouG+7mxeKvERo1QbOUEn7QcnO+rD",
}



webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=bdc3b8bd0e3ebdb39df90bf67acbbf405d04b60065db1dfe37c6c8e938f52221"
webhook_url2 = "https://oapi.dingtalk.com/robot/send?access_token=1db293dc3b37664145df981e45ad8c1ef1d3d2574b3224fb064ff1a358c97bcf"
webhook_url3 = "https://oapi.dingtalk.com/robot/send?access_token=61cb96708c2543536319fff172477490cfc3cccb703fa73a0d168786928054f8"


# 参数头部
headersa= {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headersj = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headersb = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headersh = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headersk = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headerse = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}

headersc = {
  "Host": "jsapp.jussyun.com",
  "Connection": "keep-alive",
  "device_type": "microsoft",
  "fullMobile": "19370803769",
  "os_type": "wechat_mini",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "xweb_xhr": "1",
  "os_version": "Windows 10 x64",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254162e) XWEB/18163",
  "Content-Type": "application/json",
  "token": "D7X9Dsi34IfGCg8jPnR5DVbwcQ50aQ0OvwKFkzIKFJk0F7I1VkAQCWxacAp4bwq2R0BsBt3+kD0/RgXz3SfS+ed1cy1Bcb02WkmWSmZ4it2Y8c1RO14BKZqkrtXZjlW4Z9N4n6EJms4DTlx+p3+qillUooSzNpy3/ptPLnALSU4",
  "Accept": "*/*",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/146/page-frame.html",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
}



