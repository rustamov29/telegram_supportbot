# handlers/contact.py
from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_CONTACT, PHONE_NUMBER, KANAL_LINK, BOT_LINK

router = Router()

FOOTER_TEXT = f"\n\n📢 **Kanal:** {KANAL_LINK} | 🤖 **Bot:** {BOT_LINK}"

@router.message(F.text == "📞 Biz bilan aloqa")
async def contact_cmd(message: Message):
    text = (
        "📞 **Biz bilan bog'lanish bo'limi:**\n\n"
        f"👨‍💻 **Admin bilan aloqa:** {ADMIN_CONTACT}\n"
        f"📱 **Telefon raqam:** {PHONE_NUMBER}\n\n"
        "Har qanday savol va takliflaringiz bo'lsa, bemalol murojaat qilishingiz mumkin!"
        f"{FOOTER_TEXT}"
    )
    await message.answer(text, parse_mode="Markdown")