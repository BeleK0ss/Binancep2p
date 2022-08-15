import aiohttp
import asyncio
import time
import json
import math
from aiohttp_socks import ProxyConnector

trade = {
    "BUY": 1,
    "SELL": 0
}

paytlst = {
    None: None,
    "monobank": 43,
    "privatbank": 60,
    "abank": 1,
}

paytlst_revert = {
    None: None,
    43: "monobank",
    60: "privatbank",
    1: "abank",
}

# start_time = time()

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru-RU",
    "Connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded",
    "Host": "api2.bybit.com",
    "lang": "ru-RU",
    "Origin": "https://www.bybit.com",
    "platform": "PC",
    "ec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Referer": "https://www.bybit.com/",
    "TE": "trailers",
    'sample_header': 'sample_value',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}


async def get_page_data(session, page, asset, tradetype, payt=None, transa=None):
    userid = None
    tokenid = asset  # BTC, USDT, BNB, ETH, etc.
    currencyid = "UAH"
    # 43 = Monobank;
    payment = paytlst[payt]  # 'monobank', 'privatbank', abank, etc.
    # 0 = ; 1 = Buy;
    side = trade[tradetype]  # "BUY": 1, "SELL": 0
    size = 10
    page = page  # 1, 2, 3, etc.
    amount = transa

    data = f"userId={userid}&tokenId={tokenid}&currencyId={currencyid}&payment={payment}&side={side}&size={size}&" \
           f"page={page}&amount={amount}"

    # data = {
    #     "asset": asset,             # BTC, USDT, BNB, ETH, etc.
    #     "fiat": "UAH",
    #     "merchantCheck": False,
    #     "page": page,               # 1, 2, 3, etc.
    #     "payTypes": [payt],         # 'monobank', 'privatbank', abank, etc.
    #     "publisherType": None,
    #     "rows": 10,
    #     "tradeType": tradetype,     # BUY, SELL
    #     "transAmount": transa       # 1000 UAH
    # }

    url = 'https://api2.bybit.com/spot/api/otc/item/list'

    async with session.post(url=url, json=data, headers=headers) as response:
        rt = await response.text()
        json_acceptable_string = rt.replace("'", "_")
        data = json.loads(json_acceptable_string)
        return data['result']['items']


async def gather_data(proxy, asset, tradetype, payt=None, transa=None):
    userid = None
    tokenid = asset  # BTC, USDT, BNB, ETH, etc.
    currencyid = "UAH"
    payment = paytlst[payt]  # "monobank": 43, "privatbank": 60, "abank": 1, etc.
    side = trade[tradetype]  # "BUY": 1, "SELL": 0
    size = 10
    page = 1  # 1, 2, 3, etc.
    amount = transa

    data = f"userId={userid}&tokenId={tokenid}&currencyId={currencyid}&payment={payment}&side={side}&size={size}&" \
           f"page={page}&amount={amount}"

    url = 'https://api2.bybit.com/spot/api/otc/item/list'

    if proxy:
        connector = ProxyConnector.from_url(f'{proxy}')
    else:
        connector = None
    # connector = aiohttp.TCPConnector(limit=50)
    # connector = aiohttp.TCPConnector(limit=3, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        r = await session.post(url=url, json=data, headers=headers)
        rt = await r.text()
        jsdata = rt.replace("'", "_")
        data = json.loads(jsdata)

        pgscnt = math.ceil(data['result']['count'] / 10)
        for page in range(1, pgscnt + 1):
            task = asyncio.create_task(get_page_data(session, page, asset, tradetype, payt, transa))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def main(proxy):
    asset = ["USDT", "BTC", 'ETH']
    transa = "3600"
    payt = ['monobank', 'privatbank', 'abank']

    tasksbuy = []
    taskssell = []

    for crypto in asset:
        for reqpay in payt:
            # print(f'first: {reqpay}')
            task_buy = asyncio.create_task(
                gather_data(proxy, crypto, "BUY", reqpay, transa)
            )
            tasksbuy.append(task_buy)
        # for crypto in asset:
        for reqpay2 in payt:
            # print(reqpay2)
            task_sell = asyncio.create_task(
                gather_data(proxy, crypto, "SELL", reqpay2, transa)
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
                pass


                # res = select['price']
                # for listdata2 in get_data_sell:
                #     for query2 in listdata2:
                #         for select2 in query2:
                #             crpt1 = select['tokenName']
                #             crpt2 = select2['tokenName']
                #             if crpt1 == crpt2:
                #                 # print(f'do: {crpt1} and {crpt2}')
                #                 res2 = select2['price']
                #                 #  (a—b) / b * 100
                #                 resall = (float(res2) - float(res)) / float(res) * 100
                #                 if resall > 1:
                #                     if select['recentExecuteRate'] > 50 and select2['recentExecuteRate'] > 50:
                #                         with open('ByBit_result.txt', 'a') as f:
                #                             f.write(json.dumps(f'\n{select}\n'))
                #                             f.write(json.dumps(f'\n{select2}\n'))
                #                             # f.write(f'{select}')
                #                             # f.write(f'{select2}')
                #                             f.write(f'\n{resall}%\n')
                #                             paymntsbuy = []
                #                             paymntssell = []
                #                             for pmnts_b in select['payments']:
                #                                 if pmnts_b == select['payments']:
                #                                     paymntsbuy.append(paytlst_revert[pmnts_b])
                #                             for pmnts_s in select2['payments']:
                #                                 if pmnts_s == select['payments']:
                #                                     paymntssell.append(paytlst_revert[pmnts_s])
                #                             b_user = select['userId']
                #                             s_user = select2['userId']
                #                             b_token = select['tokenName']
                #                             s_token = select2['tokenName']
                #                             b_link = f'https://www.bybit.com/fiat/trade/otc/profile/' \
                #                                      f'{b_user}/{b_token}/UAH'
                #                             s_link = f'https://www.bybit.com/fiat/trade/otc/profile/' \
                #                                      f'{s_user}/{s_token}/UAH'
                #                             info = {
                #                                 # "BUY": select,
                #                                 # "SELL": select2,
                #                                 "Token": select['tokenName'],
                #                                 "BUY_Price": select['price'],
                #                                 "SELL_Price": select2['price'],
                #                                 "B_Payments": paymntsbuy,
                #                                 "S_Payments": paymntssell,
                #                                 "B_Link": b_link,
                #                                 "S_Link": s_link,
                #                                 "Profit": f'{resall}%'
                #                             }
                #
                #                             print(json.dumps(info, indent=4))

    # end_time = time() - start_time
    # print(end_time)


if __name__ == '__main__':
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
