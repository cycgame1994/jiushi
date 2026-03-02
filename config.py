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
# url_a = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931332204da960001241231&sign=RTJGQTY1QkY5N0Q0NUM1MzM4RkEwNDk0Q0I5MjcxMTk%3D"
# url_j = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931340149963100012455d5&sign=QTU4RDhGQzkwQUVFNUYzRDMyMzc5MjQ1NTQ3NjNDM0I%3D"# 钉钉通知地址
# url_b = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693132e14996310001244821&sign=N0M1MDBBMTBDQkNCOEM4Njk1REVBMDVDNTU4ODQxMTM%3D"
# url_h = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=69315292499631000125952f&sign=MzBCMTNDRjdFNTBDQjdDOTEwREExM0NGQTZCM0MwMzc%3D"
# url_k = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693152ad4996310001259691&sign=RUI0N0ZDNUU1QjgzNzBEMTY3QzQyRUM5QjQ4QkMyMzk%3D"
# url_e = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=693152c604da960001255ee6&sign=MUU2NkIxNkNGNjA5NDg4NTg2RENFQTJEQjE3NjRBMzY%3D"
# url_c = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=wechat_mini&showId=6931535304da960001256176&sign=NjVDMTNFRDY2MTU0NUU0QUUzQTlGM0U3MTZDMzlCOTg%3D"
url_a = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=6931332204da960001241231&sign=MkMwQTAxRTczMjAyNDMyNzU0OTMxNDE4QjdCRjQ0MjY%3D"
url_j = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=6931340149963100012455d5&sign=QjNFOTZDNDkzNDVBNkE5QTRCNjcyMERCNUZGODIxOUI%3D"# 钉钉通知地址
url_b = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=693132e14996310001244821&sign=N0ZEQUZDMTI5QTUyRjE3NEUzNjA2ODA4NkRFQ0Q3OEE%3D"
url_h = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=69315292499631000125952f&sign=ODUwNDk2MEQ5RjUyQ0FBMTUzRTc3REFFNzdCMzJBMTM%3D"
url_k = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=693152ad4996310001259691&sign=NUMyOUEwMTgzMkUwRTFDQzM5QzVFMkU3QkZBM0FFNEU%3D"
url_e = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=693152c604da960001255ee6&sign=MUZGNzZCNzY2RTE0NzQ3N0I3NTlFN0I5NzE4OTE4MTQ%3D"
url_c = "https://jsapp.jussyun.com/jiushi-ticket/ticket/v2-get/getShowSessionNew?inWhite=false&os_type=ios&showId=6931535304da960001256176&sign=NjZCMjBFNjY5RDhGMDYzMEY5MzEwRDQxQzQyMzQ0MDE%3D"

# cookies
cookies = {
  "acw_tc": "0a05731817723597552226091e19e9db17e33fc029a7d72df64bdc9c65d573",
  "cdn_sec_tc": "b4a3cf0d17723597551117913ecf222bffc38499760def8bd268ae3ff3",
}
cookies2 = {
  "acw_tc": "0a05837317724147549686433e523fb9160639c75fb58c5ff44b33848147d3",
  "cdn_sec_tc": "3daa4f2017724147549426315e98b3efc53241ce2a985e8b846439d15a",
}
cookies3 = {
  "acw_tc": "0a05837317724147549686433e523fb9160639c75fb58c5ff44b33848147d3",
  "cdn_sec_tc": "3daa4f2017724147549426315e98b3efc53241ce2a985e8b846439d15a",
}
cookies4 = {
  "acw_tc": "0a05731417724255773453165e5681f1bbdc8e4a693a6aba56c468a069fea7",
  "cdn_sec_tc": "3daa4f2917724255773071037e456d1315477cccd2b97337f3fe93905f",
}



# 久事2026
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=bdc3b8bd0e3ebdb39df90bf67acbbf405d04b60065db1dfe37c6c8e938f52221"
# 第三个群
webhook_url2 = "https://oapi.dingtalk.com/robot/send?access_token=1db293dc3b37664145df981e45ad8c1ef1d3d2574b3224fb064ff1a358c97bcf"
# 久事体育
webhook_url3 = "https://oapi.dingtalk.com/robot/send?access_token=61cb96708c2543536319fff172477490cfc3cccb703fa73a0d168786928054f8"


# 参数头部模板（共用的 headers，fullmobile 和 token 会在请求时动态更新）
headers = {
  "Host": "jsapp.jussyun.com",
  "Content-Type": "application/json",
  "fullmobile": "",  # 占位符，请求时会动态更新为对应账号的手机号
  "Accept": "*/*",
  "Accept-Charset": "utf-8",
  "device_type": "iPhone 13<iPhone14,5>",
  "Accept-Language": "zh-CN,zh-Hans;q=0.9",
  "token": "",  # 占位符，请求时会动态更新为对应账号的 token
  "Accept-Encoding": "gzip, deflate, br",
  "app_id": "7134142a2721aa804af172b5c1d55e0c",
  "Referer": "https://9000000000000001.jsapp-intranet.jussyun.com/9000000000000001/1.0.238.0/index.html#packageTicket/TicketSelect/TicketSelectBuy?__appxPageId=2&__id__=2",
  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 26_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/23C71 Ariver/1.0.15 mPaaS/Portal WK RVKType(0) NebulaX/1.0.0",
  "Connection": "keep-alive",
  "os_version": "",
  "os_type": "ios"
}

# 账号池（每个账号存储：手机号、token、cookies）
# headers 是共用的，每次请求时会动态更新 fullmobile 和 token
# 目前只配置了一个账号，后续你可以在这里继续追加更多账号
ACCOUNT_POOL = [
  # {
  #   "name": "acc_ios_13817507462",  # 账号标识，可随便起名
  #   "mobile": "13817507462",  # 手机号
  #   "token": "iOKzFyX6B9glD0e9IQ/q0gWV90uLMCOs9LzCeovG9KbVzw22+wYX9HmRYkdjflxXdEdgHjmuAeIrXgQsdRERtHNbrHkxuGl1FpERcDCgo3Y",  # token
  #   "cookies": cookies,  # cookies
  # },
  # 后续账号示例（添加时去掉前面的注释，并补充 mobile/token/cookies）
  # {
  #   "name": "acc_ios_第二个账号",
  #   "mobile": "13800000000",  # 第二个账号的手机号
  #   "token": "第二个账号的token",  # 第二个账号的 token
  #   "cookies": cookies2,  # 第二个账号的 cookies（需要在上面定义 cookies2）
  # },
  {
    "name": "acc_ios_18942240295",
    "mobile": "18942240295",  # 第二个账号的手机号
    "token": "9TYa5XaAcynSUGDR2Aas7YyxWWDZRbRZtiIH7RMMBYl7BhgOSs/wzshhrIV2ezvnugZ9mae6KR7//L0208OSsMh7ZGsy4OCaSfYBibirc/g",  # 第二个账号的 token
    "cookies": cookies2,  # 第二个账号的 cookies（需要在上面定义 cookies2）
  },
  {
    "name": "acc_ios_19370803769",
    "mobile": "19370803769",  # 第二个账号的手机号
    "token": "adMV4MT3fMUEi1QL+FRz/MFZgwzZq6wS5RSKzZ/vzUye7SaCMUGvsXdkwzDs7oI/xhAXbqlpRt9RaPYlL5K4FTXK4oEmJcUhMWm0ZSWKtr8",  # 第二个账号的 token
    "cookies": cookies3,  # 第二个账号的 cookies（需要在上面定义 cookies3）
  },
  {
    "name": "acc_ios_18101860881",
    "mobile": "18101860881",  # 第二个账号的手机号
    "token": "ovdbO+x3b/TtuOSfSfELjvkX/npMl7urYtYA7JJLgzMLxRii4etN4W/0efu9zI2uda3BT4LOhK58mNou9rORPWRsMeHXH7M19lflAdHjCyY",  # 第二个账号的 token
    "cookies": cookies4,  # 第二个账号的 cookies（需要在上面定义 cookies4）
  },
]





