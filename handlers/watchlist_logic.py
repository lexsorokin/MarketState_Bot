from databases.crypto_db import CryptoFavorites
from databases.users_db import User
from keyboards.market_options_kb import market_options_keyboard
from keyboards.scroll_through_results_kb import top_ten_result_mark_up
from loader import MarketState_bot
from market_parsers.binance_parser.binance_parser import binance_parser_for_watchlist
from user_search_configuration.user_search_config import UserSearchConfig


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data.split('_')[0] == 'addToWatchList')
def save_data_to_favorites(callback):
    user_search_config = UserSearchConfig.get_user(user_id=callback.message.chat.id)
    if callback.data.split('_')[1] == 'crypto':
        if CryptoFavorites.get_or_none(
                CryptoFavorites.user_id == callback.message.chat.id and CryptoFavorites.token_ticker == user_search_config.data_for_watchlist) is None:
            user = User.get(user_id=callback.message.chat.id)
            CryptoFavorites.create(user=user,
                                   token_ticker=user_search_config.data_for_watchlist)
            MarketState_bot.answer_callback_query(callback.id, text='Coin saved to WatchList')
        else:
            MarketState_bot.answer_callback_query(callback.id, text='Coin is already in your WatchList')


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data == 'to_watchlist_folders')
def get_watchlist_folders_by_markets(callback):
    markup = market_options_keyboard(watchlist_options=True, search=False)
    MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                 text='Select WatchList FOLDER',
                                 reply_markup=markup)


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data in ['crypto_watchlist',
                                                                                'forex_watchlist',
                                                                                'stock_watchlist'
                                                                                ])
def display_watchlist_results(callback):
    user_search_config = UserSearchConfig.get_user(callback.message.chat.id)
    user_search_config.step = 1

    if callback.data == 'crypto_watchlist':
        user = User.get(user_id=callback.message.chat.id)

        watchlist_ticker_data = [
            data.token_ticker
            for data in CryptoFavorites.select().where(CryptoFavorites.user == user)
        ]

        if len(watchlist_ticker_data) != 0:

            watchlist_data = binance_parser_for_watchlist(watchlist_ticker_data)
            user_search_config.final_data = watchlist_data

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=False,
                next=True,
                add_to_watchlist=False,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]]),
                next_prev_function='watchlist_result'
            )
            MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                         text=user_search_config.final_data['display_data'][
                                             user_search_config.step - 1],
                                         reply_markup=mark_up)
        else:
            mark_up = market_options_keyboard(watchlist_options=True, search=True)
            MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                         text='Your crypto WatchList folder is empty.\n'
                                              'Proceed to SEARCH or select ANOTHER WatchList folder',
                                         reply_markup=mark_up)


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data in ['next_watchlist_result',
                                                                                'prev_watchlist_result'])
def scroll_through_search_results(callback):
    user_search_config = UserSearchConfig.get_user(callback.message.chat.id)
    if callback.data == 'next_watchlist_result':
        user_search_config.step += 1
        if user_search_config.step < len(user_search_config.final_data['display_data']):

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=True,
                add_to_watchlist=False,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]]),
                next_prev_function='watchlist_result'
            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)

        elif user_search_config.step == len(user_search_config.final_data['display_data']):

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=False,
                add_to_watchlist=False,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]]),
                next_prev_function='watchlist_result'
            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)

    elif callback.data == 'prev_watchlist_result':
        user_search_config.step -= 1

        if user_search_config.step > 1:
            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=True,
                add_to_watchlist=False,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]]),
                next_prev_function='watchlist_result'
            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)

        elif user_search_config.step == 1:

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=False,
                next=True,
                add_to_watchlist=False,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]]),
                next_prev_function='watchlist_result'
            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)
