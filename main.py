import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

import config
from database.db_handler import DatabaseHandler
from services.digiflazz import DigiflazzAPI

# Import handlers
from handlers import start, deposit, admin, transaction, history

# Import webhook server
import uvicorn
from webhook.server import app as webhook_app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Register routers
dp.include_router(start.router)
dp.include_router(deposit.router)
dp.include_router(admin.router)
dp.include_router(transaction.router)
dp.include_router(history.router)

async def set_bot_commands():
    """Set bot commands"""
    commands = [
        BotCommand(command="start", description="Mulai bot"),
        BotCommand(command="menu", description="Tampilkan menu utama"),
        BotCommand(command="tambahsaldo", description="[Admin] Tambah saldo user"),
        BotCommand(command="broadcast", description="[Admin] Broadcast pesan"),
    ]
    await bot.set_my_commands(commands)

async def refresh_products():
    """Refresh product list from Digiflazz"""
    logger.info("Refreshing product list from Digiflazz...")
    
    digiflazz = DigiflazzAPI()
    db = DatabaseHandler()
    
    try:
        result = await digiflazz.get_price_list()
        
        if result and 'data' in result:
            products = result['data']
            await db.cache_products(products)
            logger.info(f"✅ Cached {len(products)} products")
        else:
            logger.warning("⚠️ Failed to fetch product list")
            
    except Exception as e:
        logger.error(f"❌ Error refreshing products: {e}")

async def periodic_refresh():
    """Periodically refresh products every 6 hours"""
    while True:
        try:
            await refresh_products()
            # Wait 6 hours
            await asyncio.sleep(6 * 60 * 60)
        except Exception as e:
            logger.error(f"Error in periodic refresh: {e}")
            await asyncio.sleep(60)  # Retry after 1 minute on error

async def on_startup():
    """On bot startup"""
    logger.info("🚀 Starting bot...")
    
    # Initialize database
    db = DatabaseHandler()
    await db.init_db()
    logger.info("✅ Database initialized")
    
    # Set bot commands
    await set_bot_commands()
    logger.info("✅ Bot commands set")
    
    # Initial product refresh
    await refresh_products()
    
    # Start periodic refresh
    asyncio.create_task(periodic_refresh())
    
    logger.info("✅ Bot started successfully!")
    logger.info(f"Admin User ID: {config.ADMIN_USER_ID}")

async def on_shutdown():
    """On bot shutdown"""
    logger.info("Shutting down bot...")
    await bot.session.close()

async def run_webhook_server():
    """Run FastAPI webhook server"""
    config_uvicorn = uvicorn.Config(
        webhook_app,
        host="0.0.0.0",
        port=config.WEBHOOK_PORT,
        log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

async def main():
    """Main function"""
    # Startup
    await on_startup()
    
    # Run webhook server and bot polling concurrently
    if config.WEBHOOK_HOST:
        logger.info(f"🌐 Starting webhook server on port {config.WEBHOOK_PORT}")
        logger.info(f"📡 Webhook URL: {config.WEBHOOK_HOST}{config.WEBHOOK_PATH}")
        
        await asyncio.gather(
            dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
            run_webhook_server()
        )
    else:
        logger.info("📱 Running in polling mode (webhook disabled)")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")