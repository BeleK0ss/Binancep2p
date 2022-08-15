import aiohttp
import asyncio
import time
import json
import math

import requests
from aiohttp_socks import ProxyConnector


# start_time = time()


async def get_page_data(getsession, getpage, getasset, gettradet, getpayt, gettrans):
    data = {
        "asset": getasset,
        "fiat": "UAH",
        "merchantCheck": False,
        "page": getpage,
        "payTypes": [getpayt],  # 'monobank', 'privatbank'
        "publisherType": None,
        "rows": 10,
        "tradeType": gettradet,
        "transAmount": gettrans
    }

    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    async with getsession.post(url=url, json=data) as response:
        rt = await response.text()
        json_acceptable_string = rt.replace("'", "_")
        data = json.loads(json_acceptable_string)
        return data['data']


async def gather_data(proxy, assets, tradetypes, setpayt=None):
    data = {
        "asset": assets,
        "fiat": "UAH",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [setpayt],  # 'monobank', 'privatbank'
        "publisherType": None,
        "rows": 10,
        "tradeType": tradetypes,
        "transAmount": transa
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    if proxy:
        connector = ProxyConnector.from_url(f'{proxy}')
    else:
        connector = None
    # connector = aiohttp.TCPConnector(limit=50)
    # connector = aiohttp.TCPConnector(limit=3, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        async with session.post(url=url, json=data, headers=headers) as response:
            rt = await response.text()
            jsdata = rt.replace("'", "_")
            data = json.loads(jsdata)
            pgscnt = math.ceil(data['total'] / 10)

        for page in range(1, pgscnt + 1):
            task = asyncio.create_task(get_page_data(session, page, assets, tradetypes, setpayt, transa))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def main(proxy):
    tasksbuy = []
    taskssell = []

    for crypto in asset:
        for reqpay in payt:
            # print(f'first: {reqpay}')
            task_buy = asyncio.create_task(
                gather_data(proxy, crypto, "BUY", reqpay)
            )
            tasksbuy.append(task_buy)
        # for crypto in asset:
        for reqpay2 in payt:
            # print(reqpay2)
            task_sell = asyncio.create_task(
                gather_data(proxy, crypto, "SELL", reqpay2)
            )
            taskssell.append(task_sell)

    get_data_buy = await asyncio.gather(*tasksbuy)
    # print(len(get_data_buy))
    get_data_sell = await asyncio.gather(*taskssell)
    # print(len(get_data_sell))
    # task1 = await task_1
    # # print(task1[1])
    # task2 = await task_2
    # # print(task2[1])

    for listdata in get_data_buy:
        for query in listdata:
            for select in query:
                res = select['adv']['price']
                for listdata2 in get_data_sell:
                    for query2 in listdata2:
                        for select2 in query2:
                            crpt1 = select['adv']['asset']
                            crpt2 = select2['adv']['asset']
                            if crpt1 == crpt2:

                                # print(f'do: {crpt1} and {crpt2}')
                                res2 = select2['adv']['price']
                                #  (a—b) / b * 100
                                resall = (float(res2) - float(res)) / float(res) * 100
                                if resall > 1:
                                    with open('Binance_result.txt', 'a') as f:
                                        f.write(json.dumps(f'\n{select}\n'))
                                        f.write(json.dumps(f'\n{select2}\n'))
                                        # f.write(f'{select}')
                                        # f.write(f'{select2}')
                                        f.write(f'\n{resall}%\n')
                                        print(select)
                                        print(select2)
                                        print(f'{resall}%')

    # end_time = time() - start_time
    # print(end_time)


if __name__ == '__main__':
    asset = ["USDT", "BTC", 'ETH', "BUSD", "BNB"]
    transa = "3600"
    payt = ['monobank', 'privatbank', 'abank', 'ukrsibbank']
    b = True
    prx_http = None
    count = 0
    while b:
        try:
            asyncio.run(main(prx_http))
            print('wait 5 sec')
            time.sleep(5)
        except Exception:
            if count == 0:
                prx_http = 'http://176.37.187.142:24573'
                print(f'Proxy modified to {prx_http}')
                count += 1
                print('wait 5 sec')
                time.sleep(5)
                pass
            elif count == 1:
                prx_http = 'http://46.4.89.58:24573'
                print(f'Proxy modified to {prx_http}')
                count += 1
                print('wait 5 sec')
                time.sleep(5)
                pass
            else:
                count = 0
                prx_http = None
                print(f'Proxy modified to Default')
                print('wait 5 sec')
                time.sleep(5)
                pass
