"""# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, INITIAL_OWNER_ID
import database as db

from handlers import start, contact, feedback, admin

logging.basicConfig(level=logging.INFO)

async def main():   
    await db.init_db(INITIAL_OWNER_ID)
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Routerlarni loyihaga ulash
    dp.include_router(start.router)
    dp.include_router(contact.router)
    dp.include_router(feedback.router)
    dp.include_router(admin.router)
    
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())"""




"""# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database as db
from handlers import start, rating, admin, contact

logging.basicConfig(level=logging.INFO)

async def main():
    await db.create_tables()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(rating.router)
    dp.include_router(admin.router)
    dp.include_router(contact.router)
    
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())"""




# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import database as db
from handlers import start, rating, admin, contact

logging.basicConfig(level=logging.INFO)

async def main():
    # Bazani ishga tushiramiz
    await db.create_tables()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # ROUTERLARNI ULASH (Aynan shu tartibda bo'lishi kerak):
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(rating.router)   # <--- Baholash va yulduzchalar handleri shu
    dp.include_router(contact.router)
    
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








