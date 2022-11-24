from telebot import types


def top_ten_result_mark_up(text=None,
                           prev=False,
                           next=False,
                           pair=None,
                           market=None,
                           add_to_watchlist=False,
                           full_coin_name=None,
                           next_prev_function='result'):
    mark_up = types.InlineKeyboardMarkup(row_width=3)

    btn = types.InlineKeyboardButton(text=text, callback_data=text)
    next_btn = types.InlineKeyboardButton(text='>', callback_data=f'next_{next_prev_function}')
    prev_btn = types.InlineKeyboardButton(text='<', callback_data=f'prev_{next_prev_function}')
    trade_btn = types.InlineKeyboardButton(text='Trade', url=f'https://www.binance.com/en/trade/{pair}')
    add_to_watchlist_btn = types.InlineKeyboardButton(text='Add to WatchList', callback_data=f'addToWatchList_{market}')
    cmk = types.InlineKeyboardButton(text='CoinMarketCap', url=f'https://coinmarketcap.com/currencies/{full_coin_name}')
    exit = types.InlineKeyboardButton(text='Exit', callback_data='exit')

    if prev and not next:
        mark_up.add(prev_btn, btn)
        if not add_to_watchlist:
            mark_up.add(cmk, trade_btn)
        else:
            mark_up.add(cmk, add_to_watchlist_btn, trade_btn)
        mark_up.add(exit)
    elif next and not prev:
        mark_up.add(btn, next_btn)
        if not add_to_watchlist:
            mark_up.add(cmk, trade_btn)
        else:
            mark_up.add(cmk, add_to_watchlist_btn, trade_btn)
        mark_up.add(exit)
    elif prev and next:
        mark_up.add(prev_btn, btn, next_btn)
        if not add_to_watchlist:
            mark_up.add(cmk, trade_btn)
        else:
            mark_up.add(cmk, add_to_watchlist_btn, trade_btn)
        mark_up.add(exit)
    return mark_up
