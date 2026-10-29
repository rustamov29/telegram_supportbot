"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from states.states import FeedbackState, ReplyState
from config import KANAL_LINK, BOT_LINK

router = Router()
FOOTER_TEXT = f"\n\n📢 Kanal: {KANAL_LINK} | 🤖 Bot: {BOT_LINK}"

# ⚠️ O'zingizning Telegram ID'ingizni tekshirib qo'ying
OWNER_ID = 1299498580

@router.message(F.text == "✍️ Fikr va taklif bildirish")
async def feedback_start(message: Message, state: FSMContext):
    template_text = (
        "📝 Fikr va taklifingizni quyidagi namunaga asosan yozishingizni so‘raymiz:\n\n"
        "Assalomu alaykum!\n"
        "Men [O'quvchi ismi]ning onasi/dadasiman. (Agar o‘quvchining o‘zi yozayotgan bo‘lsa, ushbu qatorni qoldirishingiz mumkin.)\n"
        "Men (yoki o'zim) [Ustoz ismi] ustozning [Hafta kunlari] va [Dars kunlari] kunlari, soat [00:00] da bo‘lib o‘tadigan darslarida qatnashaman.\n\n"
        "Fikrim:\n"
        "Taklif va mulohazalaringizni erkin yozishingiz mumkin. Sizning fikringiz biz uchun juda muhim va ta'lim sifatini yanada yaxshilashga yordam beradi. ❤️\n\n"
        f"Hurmat bilan, {KANAL_LINK} oilasi. 🌿"
        f"{FOOTER_TEXT}"
    )
    await message.answer(template_text)
    await state.set_state(FeedbackState.waiting_for_text)

@router.message(FeedbackState.waiting_for_text)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.full_name or "Foydalanuvchi"
    
    try:
        feedback_id = await db.add_feedback(user_id, message.text)
    except Exception:
        feedback_id = user_id  # Zaxira ID

    await state.clear()
    await message.answer(f"✅ Rahmat! Sizning fikringiz administratsiyaga yetkazildi.{FOOTER_TEXT}")

    # Har qanday foydalanuvchida 100% ishlaydigan profil havolasi
    user_link = f"tg://user?id={user_id}"

    # Inline tugmalarda Callback Data rating.py bilan bir xil "reply:" (ikki nuqta) qilindi
    inline_btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}"),
            InlineKeyboardButton(text="👤 Profili", url=user_link)
        ]
    ])

    admin_text = (
        f"📩 <b>Yangi fikr/taklif (#ID_{feedback_id}):</b>\n\n"
        f"{message.text}\n\n"
        f"👤 <b>Yuboruvchi:</b> <a href='{user_link}'>{user_name}</a>\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    # Adminlar + Owner ro'yxati
    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)

    for admin_id in recipients:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=inline_btn,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Admin {admin_id} ga xabar yuborishda xato: {e}")

# Callback formatini rating.py bilan bir xil "reply:" ga mosladik
@router.callback_query(F.data.startswith("reply:"))
async def handle_reply_callback(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target_user_id=target_id)
    await call.message.answer("✍️ Foydalanuvchiga yubormoqchi bo'lgan javobingizni yozing:")
    await state.set_state(ReplyState.waiting_for_reply)
    await call.answer()

@router.message(ReplyState.waiting_for_reply)
async def send_reply(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_id = data.get("target_user_id")
    await state.clear()
    
    try:
        await bot.send_message(
            chat_id=target_id,
            text=f"✉️ Super Kitobxon Administratsiyasidan javob:\n\n{message.text}{FOOTER_TEXT}"
        )
        await message.answer("✅ Javobingiz muvaffaqiyatli yetkazildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yetkazishda xatolik: {e}")"""






"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from states.states import FeedbackState, ReplyState
from config import KANAL_LINK, BOT_LINK

router = Router()
FOOTER_TEXT = f"\n\n📢 Kanal: {KANAL_LINK} | 🤖 Bot: {BOT_LINK}"

# Telegram ID'ingiz (Owner)
OWNER_ID = 1299498580

@router.message(F.text == "✍️ Fikr va taklif bildirish")
async def feedback_start(message: Message, state: FSMContext):
    template_text = (
        "📝 Fikr va taklifingizni quyidagi namunaga asosan yozishingizni so‘raymiz:\n\n"
        "Assalomu alaykum!\n"
        "Men [O'quvchi ismi]ning onasi/dadasiman. (Agar o‘quvchining o‘zi yozayotgan bo‘lsa, ushbu qatorni qoldirishingiz mumkin.)\n"
        "Men (yoki o'zim) [Ustoz ismi] ustozning [Hafta kunlari] va [Dars kunlari] kunlari, soat [00:00] da bo‘lib o‘tadigan darslarida qatnashaman.\n\n"
        "Fikrim:\n"
        "Taklif va mulohazalaringizni erkin yozishingiz mumkin. Sizning fikringiz biz uchun juda muhim va ta'lim sifatini yanada yaxshilashga yordam beradi. ❤️\n\n"
        f"Hurmat bilan, {KANAL_LINK} oilasi. 🌿"
        f"{FOOTER_TEXT}"
    )
    await message.answer(template_text)
    await state.set_state(FeedbackState.waiting_for_text)

@router.message(FeedbackState.waiting_for_text)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.full_name or "Foydalanuvchi"
    
    try:
        feedback_id = await db.add_feedback(user_id, message.text)
    except Exception:
        feedback_id = user_id

    await state.clear()
    await message.answer(f"✅ Rahmat! Sizning fikringiz administratsiyaga yetkazildi.{FOOTER_TEXT}")

    # Username bor bo'lsa HTML link, bo'lmasa oddiy ism (Parser xatosi olib tashlandi)
    if message.from_user.username:
        user_link_html = f"<a href='https://t.me/{message.from_user.username}'>{user_name}</a>"
    else:
        user_link_html = f"<b>{user_name}</b>"

    admin_text = (
        f"📩 <b>Yangi fikr/taklif (#ID_{feedback_id}):</b>\n\n"
        f"{message.text}\n\n"
        f"👤 <b>Yuboruvchi:</b> {user_link_html}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    # Inline tugmalar (Username yo'q bo'lsa xavfsiz holatda faqat Javob berish tugmasi chiqadi)
    inline_buttons = [
        [InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}")]
    ]
    
    if message.from_user.username:
        inline_buttons[0].append(
            InlineKeyboardButton(text="👤 Profili", url=f"https://t.me/{message.from_user.username}")
        )

    inline_btn = InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    # Adminlar + Owner
    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)

    for admin_id in recipients:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=inline_btn,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            print(f"✅ Feedback adminga bordi: {admin_id}")
        except Exception as e:
            print(f"❌ Admin {admin_id} ga xabar yuborishda xato: {e}")

# JAVOB BERISH TUGMASI HAKOMATI
@router.callback_query(F.data.startswith("reply:"))
async def handle_reply_callback(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target_user_id=target_id)
    await call.message.answer(f"✍️ Foydalanuvchiga (ID: {target_id}) yubormoqchi bo'lgan javobingizni yozing:")
    await state.set_state(ReplyState.waiting_for_reply)
    await call.answer()

# FOYDALANUVCHIGA JAVOB YUBORISH
@router.message(ReplyState.waiting_for_reply)
async def send_reply(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_id = data.get("target_user_id")
    await state.clear()
    
    try:
        await bot.send_message(
            chat_id=target_id,
            text=f"✉️ **Administratsiyadan javob:**\n\n{message.text}{FOOTER_TEXT}",
            parse_mode="Markdown"
        )
        await message.answer("✅ Javobingiz muvaffaqiyatli yetkazildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yetkazishda xatolik: {e}")"""




from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from states.states import FeedbackState, ReplyState
from config import KANAL_LINK, BOT_LINK

router = Router()
FOOTER_TEXT = f"\n\n📢 Kanal: {KANAL_LINK} | 🤖 Bot: {BOT_LINK}"

OWNER_ID = 1299498580

@router.message(F.text == "✍️ Fikr va taklif bildirish")
async def feedback_start(message: Message, state: FSMContext):
    template_text = (
        "📝 Fikr va taklifingizni quyidagi namunaga asosan yozishingizni so‘raymiz:\n\n"
        "Assalomu alaykum!\n"
        "Men [O'quvchi ismi]ning onasi/dadasiman. (Agar o‘quvchining o‘zi yozayotgan bo‘lsa, ushbu qatorni qoldirishingiz mumkin.)\n"
        "Men (yoki o'zim) [Ustoz ismi] ustozning [Hafta kunlari] va [Dars kunlari] kunlari, soat [00:00] da bo‘lib o‘tadigan darslarida qatnashaman.\n\n"
        "Fikrim:\n"
        "Taklif va mulohazalaringizni erkin yozishingiz mumkin. Sizning fikringiz biz uchun juda muhim va ta'lim sifatini yanada yaxshilashga yordam beradi. ❤️\n\n"
        f"Hurmat bilan, {KANAL_LINK} oilasi. 🌿"
        f"{FOOTER_TEXT}"
    )
    await message.answer(template_text)
    await state.set_state(FeedbackState.waiting_for_text)

@router.message(FeedbackState.waiting_for_text)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.full_name or "Foydalanuvchi"
    
    try:
        feedback_id = await db.add_feedback(user_id, message.text)
    except Exception:
        feedback_id = user_id

    await state.clear()
    await message.answer(f"✅ Rahmat! Sizning fikringiz administratsiyaga yetkazildi.{FOOTER_TEXT}")

    if message.from_user.username:
        user_link_html = f"<a href='https://t.me/{message.from_user.username}'>{user_name}</a>"
        profile_btn = InlineKeyboardButton(
            text="👤 Profili", 
            url=f"https://t.me/{message.from_user.username}"
        )
    else:
        user_link_html = f"<b>{user_name}</b>"
        profile_btn = InlineKeyboardButton(
            text="👤 Profili", 
            callback_data=f"show_profile:{user_id}"
        )

    admin_text = (
        f"📩 <b>Yangi fikr/taklif (#ID_{feedback_id}):</b>\n\n"
        f"{message.text}\n\n"
        f"👤 <b>Yuboruvchi:</b> {user_link_html}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    inline_buttons = [
        [
            InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}"),
            profile_btn
        ]
    ]

    inline_btn = InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)

    for admin_id in recipients:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=inline_btn,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"❌ Admin {admin_id} ga xabar yuborishda xato: {e}")

@router.callback_query(F.data.startswith("reply:"))
async def handle_reply_callback(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target_user_id=target_id)
    await call.message.answer(f"✍️ Foydalanuvchiga (ID: {target_id}) yubormoqchi bo'lgan javobingizni yozing:")
    await state.set_state(ReplyState.waiting_for_reply)
    await call.answer()

@router.message(ReplyState.waiting_for_reply)
async def send_reply(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_id = data.get("target_user_id")
    await state.clear()
    
    try:
        await bot.send_message(
            chat_id=target_id,
            text=f"✉️ **Administratsiyadan javob:**\n\n{message.text}{FOOTER_TEXT}",
            parse_mode="Markdown"
        )
        await message.answer("✅ Javobingiz muvaffaqiyatli yetkazildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yetkazishda xatolik: {e}")

# Username'siz foydalanuvchining Profil tugmasi bosilganda
@router.callback_query(F.data.startswith("show_profile:"))
async def handle_show_profile(call: CallbackQuery):
    target_id = call.data.split(":")[1]
    profile_link = f"<a href='tg://user?id={target_id}'>Foydalanuvchi profilini ochish 🔗</a>"
    
    info_text = (
        f"👤 <b>Foydalanuvchi ma'lumoti:</b>\n\n"
        f"🆔 <b>ID:</b> <code>{target_id}</code>\n"
        f"⚠️ <i>Ushbu foydalanuvchida public @username o'rnatilmagan.</i>\n\n"
        f"👉 Profilga o'tish uchun bosing: {profile_link}"
    )
    await call.message.answer(info_text, parse_mode="HTML", disable_web_page_preview=True)
    await call.answer()