import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))

# Digiflazz Configuration
DIGIFLAZZ_USERNAME = os.getenv("DIGIFLAZZ_USERNAME")
DIGIFLAZZ_API_KEY = os.getenv("DIGIFLAZZ_API_KEY")
DIGIFLAZZ_WEBHOOK_SECRET = os.getenv("DIGIFLAZZ_WEBHOOK_SECRET")

# Profit Configuration
PROFIT_MARGIN = int(os.getenv("PROFIT_MARGIN", "2000"))

# Bank Account Configuration
BANK_NAME = os.getenv("BANK_NAME", "BCA")
BANK_ACCOUNT_NUMBER = os.getenv("BANK_ACCOUNT_NUMBER", "1234567890")
BANK_ACCOUNT_NAME = os.getenv("BANK_ACCOUNT_NAME", "Nama Pemilik Rekening")

# Webhook Configuration
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/digiflazz")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./ppob_bot.db")

# Digiflazz API URLs
DIGIFLAZZ_BASE_URL = "https://api.digiflazz.com/v1"
DIGIFLAZZ_PRICE_LIST_URL = f"{DIGIFLAZZ_BASE_URL}/price-list"
DIGIFLAZZ_TRANSACTION_URL = f"{DIGIFLAZZ_BASE_URL}/transaction"