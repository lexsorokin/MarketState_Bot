from telebot import types


def start_keyboard(to_watchlist=False):
    mark_up = types.InlineKeyboardMarkup(row_width=1)
    search = types.InlineKeyboardButton(text='Search', callback_data='proceed_to_markets')
    to_watchlist_btn = types.InlineKeyboardButton(text='My WatchList', callback_data='to_watchlist_folders')
    help_btn = types.InlineKeyboardButton(text='Help', callback_data='help')

    if not to_watchlist:
        mark_up.add(search, help_btn)

    else:
        mark_up.add(search, to_watchlist_btn, help_btn)

    return mark_up
