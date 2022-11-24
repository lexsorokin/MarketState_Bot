from market_parsers.binance_parser import binance_parser
from keyboards.exit_and_manual_search_kb import exit_search_keyboard
from user_search_configuration.user_search_config import UserSearchConfig
from loader import MarketState_bot


@MarketState_bot.callback_query_handler(func=lambda callback: callback.data == 'manual_search')
def manual_search(callback):
    if callback.data == 'manual_search':
        token_input = MarketState_bot.send_message(chat_id=callback.message.chat.id,
                                                   text='Type in a TICKER (BTC) or a FULL NAME (Bitcoin) of a token '
                                                        'to initiate manual search\n')
        MarketState_bot.register_next_step_handler(token_input, manual_search_result)


def manual_search_result(message):
    if not message.text.isalpha():
        not_alpha_error = MarketState_bot.send_message(chat_id=message.chat.id,
                                                       text='Please make sure that your your input is in TEXT.')
        MarketState_bot.register_next_step_handler(not_alpha_error, manual_search_result)
    else:

        final_data = binance_parser(name=message.text,
                                    search_method='manual_search')
        mark_up = exit_search_keyboard(exit=True,
                                       add_to_fav=True,
                                       trade=True,
                                       row_width=2,
                                       market='crypto',
                                       pair=''.join(
                                           [final_data['trade_data'][0][:-4],
                                            '_',
                                            final_data['trade_data'][0][-4:]]
                                       )
                                       )

        user_search_config = UserSearchConfig.get_user(user_id=message.chat.id)
        user_search_config.data_for_watchlist = message.text
        MarketState_bot.send_message(chat_id=message.chat.id,
                                     text=final_data['display_data'][0],
                                     reply_markup=mark_up)
