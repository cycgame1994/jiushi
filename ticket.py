import random
import json
from datetime import datetime
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

# 请求计数器（按通道区分）
account_a = 0
account_j = 0
account_d = 0
account_b = 0
account_h = 0
account_k = 0
account_e = 0
account_c = 0

# 发送钉钉通知
def send_dingdingbot(tickets_info):
    """发送合并后的有票信息到钉钉"""
    # 组装消息体
    message = {
        "msgtype": "text",  # 消息类型
        "text": {
            "content": f"🎫 有票通知\n{tickets_info}"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # 发送POST请求到钉钉机器人接口
    try:
        # response = requests.post(webhook_url, data=json.dumps(message), headers=headers)
        # response2 = requests.post(webhook_url2, data=json.dumps(message), headers=headers)
        response3 = requests.post(webhook_url3, data=json.dumps(message), headers=headers)

        # if response.status_code == 200:
        #     print("✓ 钉钉通知1发送成功!")
        # else:
        #     print(f"✗ 钉钉通知1发送失败，状态码: {response.status_code}, 错误信息: {response.text}")
        #
        # if response2.status_code == 200:
        #     print("✓ 钉钉通知2发送成功!")
        # else:
        #     print(f"✗ 钉钉通知2发送失败，状态码: {response2.status_code}, 错误信息: {response2.text}")

        if response3.status_code == 200:
            print("✓ 钉钉通知3发送成功!")
        else:
            print(f"✗ 钉钉通知3发送失败，状态码: {response3.status_code}, 错误信息: {response3.text}")
    except Exception as e:
        print(f"发送钉钉消息时发生错误: {e}")


# 请求
async def async_post_request(session, headers, params, account_counter):
    flag = True
    while flag:
        try:
            async with session.get(url, headers=headers, params=params, ssl=False) as response:
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
                    for i in range(len(showSessionModelList)):
                        priceInfoModelList = showSessionModelList[i]['priceInfoModelList']
                        for priceInfoMode in priceInfoModelList:
                            if priceInfoMode['stock'] == 1:
                                priceName = priceInfoMode['priceName']
                                print(priceName)
                                send_dingdingbot(priceName)
                else:
                    print(f"请求失败，状态码：{response.status}")

            await asyncio.sleep(random.randint(30, 50))
            # time.sleep(random.randint(1, 5))
        except Exception as e:
            print(f"发生错误：{e}")
            await asyncio.sleep(random.randint(1, 5))


# 主函数
async def main():
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
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

