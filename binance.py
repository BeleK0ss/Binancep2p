import requests
import json
from time import time

start_time = time()

def loadpage(tradeType, countpage=1):

    data = {
        "asset": "USDT",
        "fiat": "UAH",
        "merchantCheck": False,
        "page": countpage,
        "payTypes": ['monobank'], #'monobank', 'privatbank'
        "publisherType": None,
        "rows": 10,
        "tradeType": f"{tradeType}",
        "transAmount": "1000"
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
    rt = r.text
    json_acceptable_string = rt.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    # for key, value in rt:
    #     print(key)
    #     print(value)
    return data

def getinfo(tradeType):
    count = 1
    dictadata = loadpage(tradeType, count)
    resultlist = []
    while bool(dictadata['data']) != False:

    #    if print(bool(dictadata['data'])) is not False:
        print(count)
        count += 1

        #print(dictadata)

        # for result in dictadata:
        #     print(f'{result}: {dictadata[result]}')
        for value in dictadata['data']:
            for result in value:
                print(f'{result}: {value[result]}')

        dictadata = loadpage(tradeType, count)


getinfo("BUY")

end_time = time() - start_time
print(end_time)
