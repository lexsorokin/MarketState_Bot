from market_parsers.binance_parser import binance_parser
from keyboards.scroll_through_results_kb import top_ten_result_mark_up
from user_search_configuration.user_search_config import UserSearchConfig

from loader import MarketState_bot


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data in ['top_ten_ranked',
                                                                                'top_ten_volume',
                                                                                'top_ten_gainers',
                                                                                'top_ten_losers',
                                                                                ])
def display_search_results(callback):
    user_search_config = UserSearchConfig.get_user(callback.message.chat.id)

    user_search_config.step = 1

    final_data = binance_parser(search_method=callback.data)
    print(final_data)

    user_search_config.final_data = final_data

    mark_up = top_ten_result_mark_up(
        text=str(user_search_config.step),
        prev=False,
        next=True,
        add_to_watchlist=True,
        full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
        market='crypto',
        pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                      '_',
                      user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]])
    )
    MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                 text=user_search_config.final_data['display_data'][user_search_config.step - 1],
                                 reply_markup=mark_up)
    user_search_config.data_for_watchlist = user_search_config.final_data['data_for_watchlist'][
        user_search_config.step - 1]


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data in ['next_result', 'prev_result'])
def scroll_through_search_results(callback):
    user_search_config = UserSearchConfig.get_user(callback.message.chat.id)
    if callback.data == 'next_result':
        user_search_config.step += 1
        if user_search_config.step < 10:

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=True,
                add_to_watchlist=True,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]])

            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)
            user_search_config.data_for_watchlist = user_search_config.final_data['data_for_watchlist'][
                user_search_config.step - 1]

        elif user_search_config.step == 10:

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=False,
                add_to_watchlist=True,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]])

            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)
            user_search_config.data_for_watchlist = user_search_config.final_data['data_for_watchlist'][
                user_search_config.step - 1]

    elif callback.data == 'prev_result':
        user_search_config.step -= 1

        if user_search_config.step > 1:
            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=True,
                next=True,
                add_to_watchlist=True,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]])

            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)
            user_search_config.data_for_watchlist = user_search_config.final_data['data_for_watchlist'][
                user_search_config.step - 1]

        elif user_search_config.step == 1:

            mark_up = top_ten_result_mark_up(
                text=str(user_search_config.step),
                prev=False,
                next=True,
                add_to_watchlist=True,
                full_coin_name=user_search_config.final_data['cmk_data'][user_search_config.step - 1],
                market='crypto',
                pair=''.join([user_search_config.final_data['trade_data'][user_search_config.step - 1][:-4],
                              '_',
                              user_search_config.final_data['trade_data'][user_search_config.step - 1][-4:]])

            )
            MarketState_bot.edit_message_text(chat_id=callback.message.chat.id,
                                              text=user_search_config.final_data['display_data'][
                                                  user_search_config.step - 1],
                                              message_id=callback.message.id,
                                              reply_markup=mark_up)
            user_search_config.data_for_watchlist = user_search_config.final_data['data_for_watchlist'][
                user_search_config.step - 1]



