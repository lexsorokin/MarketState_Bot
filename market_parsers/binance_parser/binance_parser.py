import json
import requests


def data_request_to_api(url):
    try:
        request = requests.get(url)
        if request.status_code == requests.codes.ok:
            data = json.loads(request.text)
            return data
    except Exception as e:
        print('Ошибка API')
        print(e)
        return None


def binance_parser(name=None, search_method=None):
    url = 'https://www.binance.com/bapi/composite/v1/public/marketing/symbol/list'
    request_data = data_request_to_api(url=url)['data']

    final_data = {
        'display_data': [],
        'trade_data': [],
        'data_for_watchlist': [],
        'cmk_data': [],
    }

    if search_method == 'top_ten_ranked' and name is None:
        sorted_data = sorted(request_data, key=lambda token: token['rank'] if token['rank'] is not None else 0)
        for data in sorted_data:
            if data['rank'] is not None:
                final_data['display_data'].append(
                    f'{data["name"]}\n'
                    f'\nFull Name - {data["fullName"]}\n'
                    f'Price: {data["price"]} USD\n'
                    f'Volume: {data["volume"]} USD\n'
                    f'Market Cap: {data["marketCap"]} USD\n'
                    f'Day Change: {round(data["dayChange"], 2)}%\n')
                final_data['trade_data'].append(
                    data['symbol']
                )
                final_data['data_for_watchlist'].append(
                    data['name']
                )
                final_data['cmk_data'].append(
                    data['fullName']
                )

                if len(final_data['cmk_data']) == 10:
                    break

    elif search_method == 'top_ten_volume' and name is None:
        sorted_data = sorted(request_data, key=lambda token: token['volume'] if token['volume'] is not None else 0,
                             reverse=True)
        for data in sorted_data:
            if data['volume'] is not None:
                final_data['display_data'].append(
                    f'{data["name"]}\n'
                    f'\nFull Name - {data["fullName"]}\n'
                    f'Price: {data["price"]} USD\n'
                    f'Volume: {data["volume"]} USD\n'
                    f'Market Cap: {data["marketCap"]} USD\n'
                    f'Day Change: {round(data["dayChange"], 2)}%\n')
                final_data['trade_data'].append(
                    data['symbol']
                )
                final_data['data_for_watchlist'].append(
                    data['name']
                )
                final_data['cmk_data'].append(
                    data['fullName']
                )

                if len(final_data['cmk_data']) == 10:
                    break

    elif search_method in ['top_ten_gainers', 'top_ten_losers'] and name is None:
        if search_method == 'top_ten_gainers':
            sorted_data = sorted(request_data,
                                 key=lambda token: token['dayChange'] if token['dayChange'] is not None else 0,
                                 reverse=True)
        elif search_method == 'top_ten_losers':
            sorted_data = sorted(request_data,
                                 key=lambda token: token['dayChange'] if token['dayChange'] is not None else 0)
        for data in sorted_data:
            if data['dayChange'] is not None:
                final_data['display_data'].append(
                    f'{data["name"]}\n'
                    f'\nFull Name - {data["fullName"]}\n'
                    f'Price: {data["price"]} USD\n'
                    f'Volume: {data["volume"]} USD\n'
                    f'Market Cap: {data["marketCap"]} USD\n'
                    f'Day Change: {round(data["dayChange"], 2)}%\n')
                final_data['trade_data'].append(
                    data['symbol']
                )
                final_data['data_for_watchlist'].append(
                    data['name']
                )
                final_data['cmk_data'].append(
                    data['fullName']
                )

                if len(final_data['cmk_data']) == 10:
                    break

    elif search_method == 'manual_search' and name is not None:

        for data in request_data:
            if data['name'] == name:
                final_data['display_data'].append(
                    f'{data["name"]}\n'
                    f'\nFull Name - {data["fullName"]}\n'
                    f'Price: {data["price"]} USD\n'
                    f'Volume: {data["volume"]} USD\n'
                    f'Market Cap: {data["marketCap"]} USD\n'
                    f'Day Change: {round(data["dayChange"], 2)}%\n')
                final_data['trade_data'].append(
                    data['symbol']
                )
                final_data['data_for_watchlist'].append(
                    data['name']
                )
                final_data['cmk_data'].append(
                    data['fullName']
                )

                if len(final_data['cmk_data']) == 10:
                    break
        return final_data

    return final_data


def binance_parser_for_watchlist(ticker_list):
    url = 'https://www.binance.com/bapi/composite/v1/public/marketing/symbol/list'
    request_data = data_request_to_api(url=url)['data']

    watchlist_data = {
        'display_data': [],
        'trade_data': [],
        'cmk_data': [],
    }

    for ticker in ticker_list:
        for data in request_data:

            if ticker == data['name']:
                watchlist_data['display_data'].append(
                    f'{data["name"]}\n'
                    f'\nFull Name - {data["fullName"]}\n'
                    f'Price: {data["price"]} USD\n'
                    f'Volume: {data["volume"]} USD\n'
                    f'Market Cap: {data["marketCap"]} USD\n'
                    f'Day Change: {round(data["dayChange"], 2)}%\n')
                watchlist_data['trade_data'].append(
                    data['symbol']
                )
                watchlist_data['cmk_data'].append(
                    data['fullName']
                )

    return watchlist_data
