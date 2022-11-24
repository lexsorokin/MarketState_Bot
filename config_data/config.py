import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TRADERNET_API_PUB_KEY = os.getenv('TRADERNET_PUBLIC_KEY')
TRADERNET_API_SEC_KEY = os.getenv('TRADERNET_SECRET_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку")
)
