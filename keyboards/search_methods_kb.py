from telebot import types


def crypto_market_search_methods_keyboard(market_for_favorites=None):
    mark_up = types.InlineKeyboardMarkup(row_width=2)
    manual_search = types.InlineKeyboardButton(text='Manual Search', callback_data='manual_search')
    top_ten_ranked = types.InlineKeyboardButton(text='Top Coins', callback_data='top_ten_ranked')
    top_ten_volume = types.InlineKeyboardButton(text='Top Coins in Volume', callback_data='top_ten_volume')
    top_ten_gainers = types.InlineKeyboardButton(text='Top Gainers', callback_data='top_ten_gainers')
    top_ten_losers = types.InlineKeyboardButton(text='Top Losers', callback_data='top_ten_losers')
    favorites_btn = types.InlineKeyboardButton(text='My Favorites', callback_data=f'view_{market_for_favorites}_favorites')
    help_btn = types.InlineKeyboardButton(text='Help', callback_data='help')
    mark_up.add(manual_search, top_ten_ranked, top_ten_gainers, top_ten_losers, top_ten_volume, favorites_btn)
    mark_up.add(help_btn)
    return mark_up
