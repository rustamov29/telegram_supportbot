"""# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import database as db
from keyboards.default import get_main_keyboard
from config import KANAL_LINK

router = Router()

@router.message(CommandStart())
@router.message(F.text == "⬅️ Bosh menyuga qaytish")
async def start_cmd(message: Message):
    await db.add_user(message.from_user.id)
    role = await db.get_user_role(message.from_user.id)
    
    start_text = (
        "📚 **Super Kitobxon o‘quv markaziga xush kelibsiz! 👋**\n\n"
        "Assalomu alaykum!\n"
        "Siz Super Kitobxon o‘quv markazining rasmiy aloqa botiga xush kelibsiz.\n"
        "Ushbu bot orqali siz:\n\n"
        "📖 Farzandingizning o‘qish jarayonini kuzatishingiz;\n"
        "📢 Muhim e'lon va yangiliklarni olishingiz;\n"
        "📅 Dars jadvali va tadbirlar haqida ma'lumot olishingiz;\n"
        "💬 O‘quv markaz ma'muriyati bilan bog‘lanishingiz mumkin.\n\n"
        "Davom etish uchun quyidagi tugmalardan birini tanlang.\n"
        "✨ Farzandingizning bilim va kelajagi biz uchun muhim!\n"
        f"Hurmat bilan, {KANAL_LINK} oilasi. 🌿"
    )
    
    markup = get_main_keyboard(role)
    await message.answer(start_text, reply_markup=markup, parse_mode="Markdown")"""







# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import database as db
from keyboards.default import get_main_keyboard
from config import INITIAL_OWNER_ID

router = Router()

@router.message(CommandStart())
@router.message(F.text == "⬅️ Bosh menyuga qaytish")
async def start_cmd(message: Message):
    user_id = message.from_user.id
    
    # 1. Avval foydalanuvchini bazaga qo'shamiz
    await db.add_user(user_id)
    
    # 2. Agar Telegram ID config'dagi INITIAL_OWNER_ID ga teng bo'lsa, avtomatik 'owner' rolini beramiz
    if user_id == INITIAL_OWNER_ID:
        await db.set_user_role(user_id, 'owner')
        role = 'owner'
    else:
        role = await db.get_user_role(user_id)
    
    start_text = (
        "📚 **Super Kitobxon o‘quv markaziga xush kelibsiz! 👋**\n\n"
        "Assalomu alaykum!\n"
        "Siz Super Kitobxon o‘quv markazining rasmiy aloqa botiga xush kelibsiz.\n\n"
        "Davom etish uchun quyidagi tugmalardan birini tanlang."
    )
    
    # 3. Rolga qarab klaviaturani yuklaymiz ('owner' yoki 'admin' bo'lsa Admin Panel chiqadi)
    markup = get_main_keyboard(role)
    await message.answer(start_text, reply_markup=markup, parse_mode="Markdown")