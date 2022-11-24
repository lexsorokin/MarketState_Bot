from databases.users_db import User
from keyboards.exit_and_manual_search_kb import exit_search_keyboard
from keyboards.market_options_kb import market_options_keyboard
from keyboards.search_methods_kb import crypto_market_search_methods_keyboard
from keyboards.start_kb import start_keyboard
from user_search_configuration.user_search_config import UserSearchConfig
from loader import MarketState_bot
from datetime import datetime


def time_of_the_day():
    date_time = datetime.now().strftime('%d of %B %Y; %H:%M')
    date_time_lst = str(date_time).split(';')
    date = date_time_lst[0]
    if int(date_time_lst[1].split(':')[0]) < 12:
        greeting = 'Good morning'
    elif 12 <= int(date_time_lst[1].split(':')[0]) <= 15:
        greeting = 'Good afternoon'
    elif 15 < int(date_time_lst[1].split(':')[0]) <= 24:
        greeting = 'Good evening'
    return greeting, date


@MarketState_bot.message_handler(commands=['start'])
def start_command(message):
    if message.text == '/start':
        mark_up = start_keyboard(to_watchlist=True)
        daytime = time_of_the_day()

        if User.get_or_none(User.user_id == message.chat.id) is None:
            user = User.create(user_id=message.chat.id,
                               username=message.from_user.username,
                               first_name=message.from_user.first_name)
            greeting = f'{daytime[0]}, {user.first_name}!\n' \
                       f'I am pleased to meet you!'
        else:
            user = User.get(user_id=message.chat.id)
            greeting = f'{daytime[0]}, {user.first_name}!\n' \
                       f"It's nice to see you again!"

        MarketState_bot.send_message(chat_id=message.chat.id,
                                     text=f'{greeting}\n'
                                          f'Today is the {daytime[1]}.\n'
                                          'This is bot is meant to help you survey various markets: Crypto, Forex and '
                                          'Stock.\n'
                                          'For documentation on the functionality of the bot press the HELP button.',
                                     reply_markup=mark_up
                                     )


@MarketState_bot.callback_query_handler(
    func=lambda callback: callback.data == 'proceed_to_markets' or callback.data == 'continue_search')
def market_options(callback):
    mark_up = market_options_keyboard(watchlist_options=False, search=False)
    MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                 text='Please select one of the listed markets⤵',
                                 reply_markup=mark_up)


@MarketState_bot.callback_query_handler(
    func=lambda callback: callback.data == 'crypto_market')
def crypto_market_search(callback):
    mark_up = crypto_market_search_methods_keyboard(market_for_favorites=[callback.data.split('_')[0]])
    MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                 text='Please select the search type\n'
                                      'If you are unsure about listed options, press the HELP button to get a better '
                                      'understanding of each of the given options.',
                                 reply_markup=mark_up)


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data in ['exit', 'discontinue_search'])
def exit_search(callback):
    user_search_config = UserSearchConfig.get_user(user_id=callback.message.chat.id)
    user_search_config.step = None
    user_search_config.final_data = None
    user_search_config.search_method = None
    user_search_config.data_for_watchlist = None

    if callback.data == 'exit':
        mark_up = exit_search_keyboard(yes=True, no=True, add_to_fav=False, exit=False, row_width=2)
        MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                     text='Would you like to continue your search?',
                                     reply_markup=mark_up)
    elif callback.data == 'discontinue_search':
        t_m_d = time_of_the_day()
        res = t_m_d[0].split()[1]
        MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                     text=f'Thank you and have a productive {res}!')



