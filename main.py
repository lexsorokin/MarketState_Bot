from loader import MarketState_bot
from handlers import search_survey_logic, manual_search, top_ten_lists, watchlist_logic

if __name__ == '__main__':
    MarketState_bot.infinity_polling()

