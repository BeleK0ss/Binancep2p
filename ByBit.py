import requests
import json


def loadpage(tradeType, page=1):
    # if tradeType == "SELL":
    #     #sell
    #     trade = 0
    # else:
    #     #buy
    #     trade = 1

    trade = {
        "BUY": 1,
        "SELL": 0
    }

    userId = None
    tokenId = "USDT"            # BTC, USDT, BNB, ETH, etc.
    currencyId = "UAH"
    # 43 = Monobank;
    payment = 43                # 'monobank', 'privatbank', abank, etc.
    ## 0 = ; 1 = Buy;
    side = trade[tradeType]     # "BUY": 1, "SELL": 0
    size = 10
    page = page                 # 1, 2, 3, etc.
    amount = 1000

    data = f"userId={userId}&tokenId={tokenId}&currencyId={currencyId}&payment={payment}&side={side}&size={size}&page={page}&amount={amount}"



    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU",
        "Connection": "keep-alive",
        "Content-Length": "80",
        "content-type": "application/x-www-form-urlencoded",
        "guid":	"46f7f8ee-b321-0715-09ca-37cdc146b39c",
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

    r = requests.post('https://api2.bybit.com/spot/api/otc/item/list', headers=headers, json=data)
    rt = r.text
    json_acceptable_string = rt.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    return data

def getinfo(tradeType):
    count = 1
    dictadata = loadpage(tradeType, count)
    print(dictadata)
    while bool(dictadata['result']['items']) is not False:

    #    if print(bool(dictadata['data'])) is not False:
        print(count)
        count += 1

        #print(dictadata)

        # for result in dictadata:
        #     print(f'{result}: {dictadata[result]}')

        for result in dictadata['result']['items']:
            print(f'{result}')

        dictadata = loadpage(tradeType, count)

getinfo("SELL")
