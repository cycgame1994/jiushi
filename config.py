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
  "acw_tc": "0a05836617725101820163284e75707541986c7a1ac16d32714b3960707777",
  "cdn_sec_tc": "3daa4f2717725101819834056ece585cac28d6f2b7c32809be2adf8786",
}
cookies2 = {
  "acw_tc": "0a05836f17725120295461933e3d62413701c0f03f482c58e97fa1873ef92c",
  "cdn_sec_tc": "3daa4f2717725101819834056ece585cac28d6f2b7c32809be2adf8786",
}
cookies3 = {
  "acw_tc": "0a05837317724147549686433e523fb9160639c75fb58c5ff44b33848147d3",
  "cdn_sec_tc": "3daa4f2017724147549426315e98b3efc53241ce2a985e8b846439d15a",
}
cookies4 = {
  "acw_tc": "0a05731417724255773453165e5681f1bbdc8e4a693a6aba56c468a069fea7",
  "cdn_sec_tc": "3daa4f2917724255773071037e456d1315477cccd2b97337f3fe93905f",
}
cookies5 = {
  "acw_tc": "0a05837a17724353148707219e3813659118a80c4caa1fabd85178cf2393ea",
  "cdn_sec_tc": "3daa4f2917724353148406520e02d2cd62cc074fd15270e01a8f5291a0",
}
cookies6 = {
  "acw_tc": "0a05837a17724353148707219e3813659118a80c4caa1fabd85178cf2393ea",
  "cdn_sec_tc": "3daa4f2917724353148406520e02d2cd62cc074fd15270e01a8f5291a0",
}
cookies7 = {
  "acw_tc": "0a05836117725004093925476e2aac88f3be124fae0d95d77e5b6a006c7c32",
  "cdn_sec_tc": "3daa4f2317725004093636165e8a69e5d2988e8c0e86611d518f7b0412",
}
cookies8 = {
  "acw_tc": "0a05836117725004093925476e2aac88f3be124fae0d95d77e5b6a006c7c32",
  "cdn_sec_tc": "3daa4f2317725004093636165e8a69e5d2988e8c0e86611d518f7b0412",
}
cookies9 = {
   "acw_tc": "0a05732417725022543803375e3927db28c71406989ec4f60ca50875a8e43e",
  "cdn_sec_tc": "3daa4f2317725004093636165e8a69e5d2988e8c0e86611d518f7b0412",
}
cookies10 = {
   "acw_tc": "0a05836f17725120295461933e3d62413701c0f03f482c58e97fa1873ef92c",
  "cdn_sec_tc": "3daa4f2717725101819834056ece585cac28d6f2b7c32809be2adf8786",
}
cookies11 = {
   "acw_tc": "b4a3cf1f17725138187856433ef121877c159be60a524c6eab9ff30347",
  "cdn_sec_tc": "b4a3cf1f17725138187856433ef121877c159be60a524c6eab9ff30347",
}
cookies12 = {
  "acw_tc": "0a05731117725211653655656e79ed44e2ac82c6c966758c54b9ed11d4be69",
  "cdn_sec_tc": "3daa4f1c17725211653275633e1dbc942c9d27e7c2934c9b33b32be72e",
}
cookies13 = {
  "acw_tc": "0a05731117727233246721762e79d4d72a8d9e7ae2d9b9fe9c51371cf93881",
  "cdn_sec_tc": "b4a3cf1e17727208245002302eb8983977ac080b2260bbbacd5cdaa0cd",
}
cookies14 = {
  "acw_tc": "0a05731917728587573611752e027b6725e8931209b32b1d2669fad31d0862",
  "cdn_sec_tc": "3daa4f2f17728587573268458e3a9380ded9650bb2838a0f7cb273d3d8",
}
cookies15 = {
  "acw_tc": "0a05837517728610227761515e4e6362537a9960be8b4e2221c7516fd64653",
  "cdn_sec_tc": "3daa4f2f17728587573268458e3a9380ded9650bb2838a0f7cb273d3d8",
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
  {
    "name": "acc_ios_17015750930",  # 账号标识，可随便起名
    "mobile": "17015750930",  # 手机号
    "token": "+/mPXmv+Qyn73w/4retGUplnmmo+Lh4DG4L4ofHppE7Q+hdaLXyRtJt546O553rfvfbQ7ETu/8SyfnmkcuJBjOGG/ZI5qgPu+W2nnppMFpU",  # token
    "cookies": cookies,  # cookies
  },
  # 后续账号示例（添加时去掉前面的注释，并补充 mobile/token/cookies）
  {
    "name": "acc2_ios_19178845510",
    "mobile": "19178845510",  # 第二个账号的手机号
    "token": "Z303HYe6oJo26ySaf+OpvYnmJ96UjFk/w0Ia1H15In23l1moiSk90LSvrewbjWNCbpFI4Y2B5kwD02Ni8YxFQf+XKTvl27c39rtbn2cdmbA",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies2）
  },
  {
    "name": "acc3_ios_17339184681",
    "mobile": "17339184681",  # 第二个账号的手机号
    "token": "A9peBjpVgQdmazwO5Jdga9nB8vUiFhMPya89LEZ9qYRzEF0AVrUfgbCHjXAXsoFYIX8eUOs9LXGTDTV82gAqHn4emXEPe953VHd7bbwjBgc",  # 第二个账号的 token
    "cookies": cookies2,  # 第二个账号的 cookies（需要在上面定义 cookies2）
  },
  {
    "name": "acc4_ios_17124372188",
    "mobile": "17124372188",  # 第二个账号的手机号
    "token": "+4dz2N9l8NPtYjF7IodX5UdVvOu5QKx/KCZpzEh51mbyhGEw6i+nCU8qyCDRCt0peI01Bsk65U8iHDBdNkRz6fPJVR4u+pKxkqcZCcNhbsE",  # 第二个账号的 token
    "cookies": cookies2,  # 第二个账号的 cookies（需要在上面定义 cookies3）
  },
  {
    "name": "acc5_ios_16521618727",
    "mobile": "16521618727",  # 第二个账号的手机号
    "token": "bjHtqxwrN+MRIrttHjOoVHETdc3VDJYED5bK0pGK4+u9J+tdPDbjyrtIWSWTy/f7X0Sbph0ABdpTWQ/ItToyl9ijSriBB53ZdJC/BKyOEc4",  # 第二个账号的 token
    "cookies": cookies2,  # 第二个账号的 cookies（需要在上面定义 cookies4）
  },
  {
    "name": "acc6_ios_19914483614",
    "mobile": "19914483614",  # 第二个账号的手机号
    "token": "4Wkcr/tUToROtELm/SqgXmEZle6VvPaS5gQv8JI+l3aUv2L51rUJlrYWJNVjiYu31hi6ilcTCxmlObmVIbq87x+ZyZNIXTh7+MAoj3XlFcA",  # 第二个账号的 token
    "cookies": cookies5,  # 第二个账号的 cookies（需要在上面定义 cookies4）
  },
  {
    "name": "acc7_ios_19372838856",
    "mobile": "19372838856",  # 第二个账号的手机号
    "token": "38O8OZOSc8aLiVKtDmfFCiVGVivcTXrwLQWpzQopMJuooM4z3zZeNiXSGGrOvLfD7S8/R5zWATuZXgbAYogOqlCXAcS0izEc90SQS97j2vs",  # 第二个账号的 token
    "cookies": cookies6,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc8_ios_17080278517",
    "mobile": "17080278517",  # 第二个账号的手机号
    "token": "E3d9xmdAqznIggOJKtnUS+RxhEbORvDfwsOfCu0f8EJp64UdSISTxXMsdxU8UMzavbTC0LgEG0ffAfCmSQtY6C5Bb3T+R3DvVBd0aTCEIAM",  # 第二个账号的 token
    "cookies": cookies7,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc9_ios_16550836018",
    "mobile": "16550836018",  # 第二个账号的手机号
    "token": "4pmzkBNbqjZTCfAPl7Tkcr4RLZf1zy7Z2/qXlMslISd7XFcxL1YmJCWRgGrpEoiqce49MpTeUwGU1jW4js1wtSndZ95reR6EjX3mF9kVOcE",  # 第二个账号的 token
    "cookies": cookies8,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc10_ios_18634270308",
    "mobile": "18634270308",  # 第二个账号的手机号
    "token": "ImzEktwW8Eoz/7go1VfboNACxQOzjsUDg/ktCsGkx7Rz3u6e3Chj99J8L2W+GcEdg+l8HYIzcztmgE5p6eElr+EHAKgsjiomRuUA4K4IdcE",  # 第二个账号的 token
    "cookies": cookies8,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc11_ios_16741676764",
    "mobile": "16741676764",  # 第二个账号的手机号
    "token": "tADFp/CMq60tauQ19bZHc9N8yFlIb7tX3CVxBe4mh53Gz5lGhMU31vLPSBGP0YI4FU6vOy7tROUm3Z6y9QkoaBbLHbj8nf41SlOKtTB/6M0",  # 第二个账号的 token
    "cookies": cookies8,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc12_ios_15130756705",
    "mobile": "15130756705",  # 第二个账号的手机号
    "token": "C5n/k8jWcNF2vLhgleCJNis2kdQKOfmDJ7qg98VOknPnnTWzQUDUBX/2Jr/hcZHvg6PeErgtmU+VqjjWH9kxN7gJup5flUsnsezkv4Sve9k",  # 第二个账号的 token
    "cookies": cookies8,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc13_ios_19949347992",
    "mobile": "19949347992",  # 第二个账号的手机号
    "token": "PFRTCToZ0X6yHtJmkeb/7ZBb1YnCFzPh5DETa1NzL7rPvTZYNZMZ2dSmadit4/6SpKeQ/fS1oKGUE5KrFnUBFhPv32btg+VmPdCYM+1ZJBo",  # 第二个账号的 token
    "cookies": cookies9,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc14_ios_17166957594",
    "mobile": "17166957594",  # 第二个账号的手机号
    "token": "bcd3sNZtgD0N0ZoZdvKJN+C2YiRT7J4DWFyF1fP4U+19HL2rQqv0GLBpGy1SxHDENzBbHZkaBhtxwmlllMm6rrOCmE3MzdLvXwPL28XLbjo",  # 第二个账号的 token
    "cookies": cookies9,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc15_ios_17153154177",
    "mobile": "17153154177",  # 第二个账号的手机号
    "token": "rZU5bG4QmNb7vWaWzoakQct3AOVIq5cC00LoUVI2M5xpyLTHLhR2hRaP/izrIdNR9ttrQhulYyjuI4mNFBLCRtsnBDerWvDOSX7hyewJW9c",  # 第二个账号的 token
    "cookies": cookies9,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc16_ios_17370345543",
    "mobile": "17370345543",  # 第二个账号的手机号
    "token": "h2rOokUZ3MrwvMMPFi8czk88qAKPJh+XiMJTKpS6bBxxd++q1EI3JlUVFR5qrdJn3mEaTjAwjKwIFl1lgMATEfdJ8b+529OvH2uCJYOHWJ4",  # 第二个账号的 token
    "cookies": cookies10,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc17_ios_16223272709",
    "mobile": "16223272709",  # 第二个账号的手机号
    "token": "YRWIaD26v5jTu3z4cTH9QI0IAUAifANzUfBZu+g2oL8mT8qcB9SPbS7+D+kojz0SXU4jfOjiJFAgYW11GdcYT5PCXfBr+horCbt1Woh645M",  # 第二个账号的 token
    "cookies": cookies13,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc18_ios_17194650193",
    "mobile": "17194650193",  # 第18个账号的手机号
    "token": "0Pkuzhs1OOqSWwXcdqg41HS1fVb6Mj/VAlnLR/RVL+wT0lrIxRKlZj2hLcsR1G6SJMNXR9EZnYF7623Eu/Vk7V78spokq4kJ2sR4UdzHmz8",  # 第二个账号的 token
    "cookies": cookies11,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc19_ios_16735967074",
    "mobile": "16735967074",  # 第19个账号的手机号
    "token": "RRujV1mDUPKY1q22nChl/d2qmA5W0jbAHhY2whwcpLI0VkcYqVOLyPePT1cF+b+xDHYc4gJx7FRpAet+3ldhQ6m7CgyNl69gJuTkb6Qv9UQ",  # 第二个账号的 token
    "cookies": cookies11,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc20_ios_17025272941",
    "mobile": "17025272941",  # 第20个账号的手机号
    "token": "z60EKxxGMUle/NtvK9mnwK5G3UV+zzbMg8zioakao7Uju5TogI0T2ZCZ81B9PzkFyckOgf4BHS0275b88iBFXvhmJnhSL+XB8mtuYBU/MsE",  # 第二个账号的 token
    "cookies": cookies11,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc21_ios_18677290314",
    "mobile": "18677290314",  # 第20个账号的手机号
    "token": "66j6Uoou7kVbmKasqonQLiGVgc0+j9wSXryRzLRuurhnmU9pH5Zjhb5zz6AGto7iR/9eDQLqtLmSJQB/skkUplrSd+2DRZIDuCaUzh7Y4Wg",  # 第二个账号的 token
    "cookies": cookies12,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc22_ios_18036579872",
    "mobile": "18036579872",  # 第20个账号的手机号
    "token": "zbfFgQOYBdkufmq4dUVnEL/L6d0vHF64mnNEqo5pqEEKb0N7E8LlKvKsI3rWm8Nup1hnEmGc7aVPSQMOXTa5mW/NOXuxzbYIzJPg5DHjGBM",  # 第二个账号的 token
    "cookies": cookies12,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc23_ios_18185271599",
    "mobile": "18185271599",  # 第20个账号的手机号
    "token": "ndDXhed3Nyx3uaV9jcjzrFI6qBNEsprep8N5O5zZKW6tY/DSQeyU3pXWEkWM61Ccu/Ccti3x9eF/aFk4d7L4mo4rwckgr5uvWMcRjvGgO5Y",  # 第二个账号的 token
    "cookies": cookies12,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc24_ios_17639903157",
    "mobile": "17639903157",  # 第20个账号的手机号
    "token": "vB+LX5izV8XG2pXf67I0oIsHMM2oP2DxHjsLnK4Obc8H+/gwYFnkiYgosZN9TWmfgl2G52WDYNn4vNmvFMF5KjPerXIsfUqPIEiyltrtOok",  # 第二个账号的 token
    "cookies": cookies12,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc25_ios_16752616041",
    "mobile": "16752616041",  # 第20个账号的手机号
    "token": "NIlabR3xtY8DjnC5RpRcsu+qOG1pIxmPAmyLRai4XWEsC9L8/hAZFLbrHtRiaKSZGTtyq7VmMvA6qxsspsPYY+uD7Ygv9e+lksTJAM/hwv4",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc26_ios_17015751697",
    "mobile": "17015751697",  # 第20个账号的手机号
    "token": "J9tN6n5Z1mPiGT6D6tts66S2I8R4c3zQTjeeRCNXw4N8aSSx21WIR95xjH1JYNshFKmbm2RmEvOybjKAUHVh4dI2tos5dQYtEkvNxIf9VwE",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc27_ios_17015856413",
    "mobile": "17015856413",  # 第20个账号的手机号
    "token": "ycBz9rMXftNKZVaN7me9dBcidcHDUG6glz6laaJ5oD0nXhT/FTqPCNAvF2u+XOK8aA9RHs84Uo63FsYaQTjRdQHwqEclB4/pzyHhBYW0G1A",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc28_ios_17080278437",
    "mobile": "17080278437",  # 第20个账号的手机号
    "token": "ZVY5BhjZivVvdhZHSJu5kghoSCujE9WL+8cV1ONfT+SpefkMj8gcYiLMg/k1WO4zLfvFwa06P4Dti1xaP8nRIkGNgqNH3pweSE5v2tqr8C0",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc29_ios_18031722691",
    "mobile": "18031722691",  # 第20个账号的手机号
    "token": "Iik5gMEawXA/QvDrHFaIgf8PjHyBt2S7dhPNkJQqrTQK+IvVHslJ5cACxfQ6RYrKA+QDBaXcGDkt/sSjirxB8dRJbjK0cHdf/VNHsBksCfs",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc30_ios_16266135865",
    "mobile": "16266135865",  # 第20个账号的手机号
    "token": "Q8uRhGrFD7vgPioEkNOvJfrtTPeUgtFDSUNDTOyy1VA3VkAkd5K0ck2NfBLdbp8FVLsybaXosW07a1zgBHQ8me7eDZSmP9o6+BhLgZUrALs",  # 第二个账号的 token
    "cookies": cookies14,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc31_ios_16267616084",
    "mobile": "16267616084",  # 第20个账号的手机号
    "token": "/8G0l7hZJk5OuSQfoJ2lZxt0c0rU+H6CP9MsvjB2CCaWAfVXgWazniFPOVZg2r3PcluPrnCwFLimluTR1JjrzDteIQjCR9wEnHBM5SHbEBQ",  # 第二个账号的 token
    "cookies": cookies15,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc32_ios_17101761824",
    "mobile": "17101761824",  # 第20个账号的手机号
    "token": "n8Usp2N8s9gHKpHo1WmCNYJ0y8KysxTRXS1NFLG6LUXC/zqM8QUh4zYZBz47vxccX/NpwpP731M/MvyxXa/E39MKdvt2c+ONSi4xLLk7sWY",  # 第二个账号的 token
    "cookies": cookies15,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc33_ios_17025279693",
    "mobile": "17025279693",  # 第20个账号的手机号
    "token": "tElmQtO9UqO51XsMlfJHFwNU5jb+hDZli3IK6RKFuCTBdyaRdfA+6VbX6AvGUlGkDC2Z/NQJN7tRRHjNfe7saywGdCAeU9zNNIqdXCzyJYk",  # 第二个账号的 token
    "cookies": cookies15,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },
  {
    "name": "acc34_ios_17100867868",
    "mobile": "17100867868",  # 第20个账号的手机号
    "token": "g/LG4HdYT3eWSb7lwECJ4nyfFFCQznrFEsR6cvXoAN7tQgW9gvr+BAgh3IK41UnUc5ebxwpi0WcelgB4ptikiKTpySr+t+7wbdjSZCa5Wvk",  # 第二个账号的 token
    "cookies": cookies15,  # 第二个账号的 cookies（需要在上面定义 cookies6）
  },



]





