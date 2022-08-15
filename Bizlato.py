import requests
import json


def loadpage():

    data = {


        "lang": "ru",
        "limit": 999,
        "skip": 0,
        "type": "selling",
        "currency": "UAH",
        "cryptocurrency": "USDT",
        "isOwnerVerificated": False,
        "isOwnerTrusted": False,
        "isOwnerActive": True,
        "amount": 100,
        "paymethod": 1111,
        "amountType": "currency", #cryptocurrency, currency
        "paymethodSlug": None


    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        # #"Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # #"Content-Length": "122",
        "content-type": "application/json",
        "Host": "bitzlato.com",
        # "ec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        # #"Pragma": "no-cache",
        # "Referer": "https://bitzlato.com",
        "TE": "Trailers",
        'sample_header': 'sample_value',
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64; rv: 102.0) Gecko/20100101 Firefox/102.0"
    }

    r = requests.get(f'https://bitzlato.com/api2/p2p/public/exchange/dsa/?lang=ru&'
                     f'limit={data["limit"]}&'
                     f'skip={data["skip"]}&'
                     f'type={data["type"]}&'
                     f'currency={data["currency"]}&'
                     f'cryptocurrency={data["cryptocurrency"]}&'
                     f'isOwnerVerificated={data["isOwnerVerificated"]}&'
                     f'isOwnerTrusted={data["isOwnerTrusted"]}&'
                     f'isOwnerActive={data["isOwnerActive"]}&'
                     f'amount={data["amount"]}&'
                     f'amountType={data["amountType"]}&'
                     f'paymethodSlug={data["paymethodSlug"]}',
                     headers=headers)
    rt = r.text
    json_acceptable_string = rt.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    # for key, value in rt:
    #     print(key)
    #     print(value)
    return print(data)

def getinfo():
    count = 1
    dictadata = loadpage()
    while bool(dictadata['data']) is not False:

    #    if print(bool(dictadata['data'])) is not False:
        print(count)
        count += 1

        #print(dictadata)

        # for result in dictadata:
        #     print(f'{result}: {dictadata[result]}')

        for result in dictadata['data'][0]:
            print(f'{result}: {dictadata["data"][0][result]}')

        dictadata = loadpage(count)


loadpage()
