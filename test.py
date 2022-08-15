import asyncio
import json

import aiohttp
from aiohttp_socks import ProxyConnector

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    "Accept-Language": "ru-RU",
    "Connection": "keep-alive",
    "content-type": "application/x-www-form-urlencoded",
    'Host': 'api2.bybit.com',
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

async def gather_data(asset, tradetype, payt=None, transa=None):
    trade = {
        "BUY": 1,
        "SELL": 0
    }

    paytlst = {
        None: None,
        "monobank": 43,
        "privatbank": 60,
        "abank": 1,
        "ukrsibbank": 80
    }

    userid = None
    tokenid = asset  # BTC, USDT, BNB, ETH, etc.
    currencyid = "UAH"
    payment = paytlst[payt]  # "monobank": 43, "privatbank": 60, "abank": 1, etc.
    side = trade[tradetype]  # "BUY": 1, "SELL": 0
    size = 10
    page = 1  # 1, 2, 3, etc.
    amount = transa

    data = f"userId={userid}&tokenId={tokenid}&currencyId={currencyid}&payment={payment}&side={side}&size={size}&page={page}&amount={amount}"
    print(data)


    url = 'https://api2.bybit.com/spot/api/otc/item/list'
    # if proxy:
    #     connector = ProxyConnector.from_url(f'{proxy}')
    # else:
    #     connector = None
    # connector = aiohttp.TCPConnector(limit=50)
    # connector = aiohttp.TCPConnector(limit=3, ssl=False)
    async with aiohttp.ClientSession() as session:

        r = await session.post(url=url, json=data)
        print(r.headers)
        print(r.connection)
        print(r.url)
        print(r.charset)
        print(r.closed)
        print(r.raw_headers)
        print(r.request_info)

        tasks = []
        r = await session.post(url=url, json=data, headers=headers)
        rt = await r.text()
        print(rt)
        jsdata = rt.replace("'", "_")
        data = json.loads(jsdata)
        print(data)




asyncio.run(gather_data("USDT", "BUY", "monobank", "3600"))
