# import PublicApiClient as NtApi
# from config_data import config
#
# pub_ = config.TRADERNET_API_PUB_KEY
# sec_ = config.TRADERNET_API_SEC_KEY
# cmd_ ='getSecurityInfo'
# pparams_ = {
#     'ticker': 'SBER',
#     'sup': True
# }
#
# res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V2)
# data = res.sendRequest(cmd_, pparams_).content.decode("utf-8")
#
# print(data)
import json

import requests


def data_request_to_api(url, parameters):
    try:
        request = requests.get(url=url, params=parameters)
        print(request.status_code)
        if request.status_code == requests.codes.ok:
            data = json.loads(request.text)
            return data
    except Exception as e:
        print('Ошибка API')
        print(e)
        return None


params = {
    "take": 10,
    "skip": 0,
    "filter": {
        "filters": [
            {
                "field": "ticker",
                "operator": "eq",
                "value": "AAPL.US"
            },
            {
                "field": "instr_type",
                "operator": "in",
                "value": "опцион, акция обыкновенная"
            }
        ]
    }
}

res = data_request_to_api(url='https://tradernet.ru/securities/ajax-get-all-securities',
                          parameters=params)
print(res)
