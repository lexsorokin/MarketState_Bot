from telebot import types


def market_options_keyboard(watchlist_options=False, search=False):
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    crypto = types.InlineKeyboardButton(text='Crypto', callback_data='crypto_market')
    forex = types.InlineKeyboardButton(text='Forex', callback_data='forex_market')
    stock = types.InlineKeyboardButton(text='Stock', callback_data='stock_market')
    crypto_favorites = types.InlineKeyboardButton(text='Crypto WatchList', callback_data=f'crypto_watchlist')
    forex_favorites = types.InlineKeyboardButton(text='Forex WatchList', callback_data=f'forex_watchlist')
    stock_favorites = types.InlineKeyboardButton(text='Stock WatchList', callback_data=f'stock_watchlist')
    search_btn = types.InlineKeyboardButton(text='Search', callback_data='proceed_to_markets')

    if not watchlist_options and not search:
        mark_up.add(crypto, forex, stock)

    elif watchlist_options and not search:
        mark_up.add(crypto_favorites, forex_favorites, stock_favorites)

    elif watchlist_options and search:
        mark_up.add(search_btn)
        mark_up.add(crypto_favorites, forex_favorites, stock_favorites)

    return mark_up
