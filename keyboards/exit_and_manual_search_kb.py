from telebot import types


def exit_search_keyboard(exit=False, add_to_fav=False, trade=False, yes=False, no=False, row_width=1, market=None, pair=None):
    mark_up = types.InlineKeyboardMarkup(row_width=row_width)
    yes_btn = types.InlineKeyboardButton(text='Yes', callback_data='continue_search')
    no_btn = types.InlineKeyboardButton(text='No', callback_data='discontinue_search')
    exit_btn = types.InlineKeyboardButton(text='Exit', callback_data='exit')
    add_to_watchlist = types.InlineKeyboardButton(text='Add to WatchList', callback_data=f'addToWatchList_{market}')
    trade_btn = types.InlineKeyboardButton(text='Trade', url=f'https://www.binance.com/en/trade/{pair}')
    if (yes and no) and (not exit and not add_to_fav):
        mark_up.add(yes_btn, no_btn)
    if (not yes and not no) and (exit and add_to_fav and trade):
        mark_up.add(add_to_watchlist, trade_btn, exit_btn)
    return mark_up