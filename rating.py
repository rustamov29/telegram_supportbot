"""# handlers/rating.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState

router = Router()

# 1. Baholash tugmasi bosilganda
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi inline tugmasi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr yozib yuborilganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzli baho tanlanganda
@router.callback_query(FeedbackRatingState.waiting_for_rating, F.data.startswith("rate_star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext):
    rating_val = int(callback.data.split(":")[1])
    data = await state.get_data()
    
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text")
    user_id = callback.from_user.id
    
    # Bazaga saqlash
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer()"""





"""# handlers/rating.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState

router = Router()

# 1. Baholash tugmasi bosilganda
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi inline tugmasi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr yozib yuborilganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzli baho tanlanganda (Har qanday holatda ham ushlab olishi uchun State filtrsiz)
@router.callback_query(F.data.startswith("rate_star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext):
    rating_val = int(callback.data.split(":")[1])
    data = await state.get_data()
    
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmadi")
    user_id = callback.from_user.id
    
    if not teacher_name:
        await callback.answer("⚠️ Seans muddati o'tgan. Iltimos, qaytadan boshlang.", show_alert=True)
        await state.clear()
        return

    # Bazaga saqlash
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")"""



"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState

router = Router()

# 1. Baholash tugmasi bosilganda
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr kelganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzcha bosilganda
@router.callback_query(F.data.startswith("star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext, bot: Bot):
    rating_val = int(callback.data.split(":")[1])
    
    data = await state.get_data()
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmagan")
    
    # Agar seans yo'qolgan bo'lsa
    if not teacher_name:
        await callback.answer("⚠️ Qaytadan o'qituvchini tanlab urinib ko'ring.", show_alert=True)
        await state.clear()
        return

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    username = f"@{callback.from_user.username}" if callback.from_user.username else "Mavjud emas"

    # 1. BAZAGA SAQLASH
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val

    # 2. FOYDALANUVCHIGA TASDIQ XABARI
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")

    # 3. ADMIN VA OWNER'LARGA XABAR YUBORISH
    admin_msg = (
        f"📩 **Yangi fikr va baho kelib tushdi!**\n\n"
        f"👤 **Foydalanuvchi:** {user_name} ({username})\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"👨‍🏫 **O'qituvchi:** {teacher_name}\n"
        f"⭐ **Baho:** {stars_display} ({rating_val}/5)\n"
        f"💬 **Fikr:** _{comment_text}_"
    )
    
    admins = await db.get_all_admins()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, admin_msg, parse_mode="Markdown")
        except Exception:
            pass"""



"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState

router = Router()

# 1. Baholash jarayonini boshlash
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr kelganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzcha bosilganda (Admin va Owner'larga xabar yuborish)
@router.callback_query(F.data.startswith("star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext, bot: Bot):
    rating_val = int(callback.data.split(":")[1])
    
    data = await state.get_data()
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmagan")
    
    if not teacher_name:
        await callback.answer("⚠️ Qaytadan o'qituvchini tanlab urinib ko'ring.", show_alert=True)
        await state.clear()
        return

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Foydalanuvchi"

    # Bazaga saqlash
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val

    # Foydalanuvchiga javob xabari
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")

    # ADMINLAR UCHUN 2-RASMDAGIDEK XABAR FORMATI
    admin_msg = (
        f"📩 **Yangi fikr/taklif (#ID_{user_id}):**\n\n"
        f"👨‍🏫 **O'qituvchi:** {teacher_name}\n"
        f"⭐ **Baho:** {stars_display} ({rating_val}/5)\n"
        f"💬 **Fikr:** {comment_text}\n\n"
        f"👤 **Yuboruvchi:** {user_name}\n"
        f"🆔 **ID:** `{user_id}`"
    )
    
    # Username'i yo'q foydalanuvchilar uchun ham to'g'ri ishlaydigan profil havolasi
    if callback.from_user.username:
        profile_url = f"https://t.me/{callback.from_user.username}"
    else:
        profile_url = f"tg://user?id={user_id}"

    # Inline tugmalar: "💬 Javob berish" va "👤 Profili"
    admin_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}"),
            InlineKeyboardButton(text="👤 Profili", url=profile_url)
        ]
    ])
    
    # Barcha adminlarga yuborish
    admins = await db.get_all_admins()
    for admin_id in admins:
        try:
            await bot.send_message(
                chat_id=admin_id, 
                text=admin_msg, 
                parse_mode="Markdown", 
                reply_markup=admin_inline_kb
            )
        except Exception:
            pass"""





"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState

router = Router()

# ⚠️ Telegram ID'ingizni tekshirib qo'ying
OWNER_ID = 1299498580  

# 1. Baholash jarayonini boshlash
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr kelganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzcha bosilganda (Bazaga saqlash va Admin/Owner'ga yuborish)
@router.callback_query(FeedbackRatingState.waiting_for_rating, F.data.startswith("star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext, bot: Bot):
    rating_val = int(callback.data.split(":")[1])
    
    data = await state.get_data()
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmagan")
    
    if not teacher_name:
        await callback.answer("⚠️ Qaytadan o'qituvchini tanlab urinib ko'ring.", show_alert=True)
        await state.clear()
        return

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Foydalanuvchi"

    # Bazaga saqlash
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val

    # Foydalanuvchiga tasdiq xabari
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")

    # Username bo'lsa ham, bo'lmasa ham to'g'ri ishlaydigan link
    user_profile_link = f"tg://user?id={user_id}"

    # Admin va Owner uchun bildirishnoma matni (HTML)
    admin_msg = (
        f"📩 <b>Yangi fikr/taklif (#ID_{user_id}):</b>\n\n"
        f"👨‍🏫 <b>O'qituvchi:</b> {teacher_name}\n"
        f"⭐ <b>Baho:</b> {stars_display} ({rating_val}/5)\n"
        f"💬 <b>Fikr:</b> {comment_text}\n\n"
        f"👤 <b>Yuboruvchi:</b> <a href='{user_profile_link}'>{user_name}</a>\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    # Inline tugmalar: "💬 Javob berish" va "👤 Profili" (Yonma-yon)
    admin_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}"),
            InlineKeyboardButton(text="👤 Profili", url=user_profile_link)
        ]
    ])
    
    # Bazadagi adminlar + Owner
    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)
    
    # Yuborish
    for recipient_id in recipients:
        try:
            await bot.send_message(
                chat_id=recipient_id, 
                text=admin_msg, 
                parse_mode="HTML", 
                reply_markup=admin_inline_kb
            )
            print(f"✅ Feedback adminga bordi: {recipient_id}")
        except Exception as e:
            print(f"❌ Admin {recipient_id} ga yuborishda xatolik: {e}")"""






"""from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState, ReplyState

router = Router()

# Telegram ID'ingiz (Owner)
OWNER_ID = 1299498580  

# 1. Baholash jarayonini boshlash
@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

# 2. O'qituvchi tanlanganda
@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

# 3. Fikr kelganda
@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

# 4. Yulduzcha bosilganda (Bazaga saqlash va Adminga yuborish)
@router.callback_query(FeedbackRatingState.waiting_for_rating, F.data.startswith("star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext, bot: Bot):
    rating_val = int(callback.data.split(":")[1])
    
    data = await state.get_data()
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmagan")
    
    if not teacher_name:
        await callback.answer("⚠️ Qaytadan o'qituvchini tanlab urinib ko'ring.", show_alert=True)
        await state.clear()
        return

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Foydalanuvchi"

    # Bazaga saqlash
    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val

    # Foydalanuvchiga tasdiq javobi
    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")

    # ------------------ YANGI O'ZGARISH QISMI ------------------
    # Username bo'lsa HTML link, bo'lmasa oddiy ism (Telegram parsing xatosi bermasligi uchun)
    if callback.from_user.username:
        user_link_html = f"<a href='https://t.me/{callback.from_user.username}'>{user_name}</a>"
    else:
        user_link_html = f"<b>{user_name}</b>"

    # Admin xabar matni
    admin_msg = (
        f"📩 <b>Yangi fikr/taklif (#ID_{user_id}):</b>\n\n"
        f"👨‍🏫 <b>O'qituvchi:</b> {teacher_name}\n"
        f"⭐ <b>Baho:</b> {stars_display} ({rating_val}/5)\n"
        f"💬 <b>Fikr:</b> {comment_text}\n\n"
        f"👤 <b>Yuboruvchi:</b> {user_link_html}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    # Inline tugmalar
    inline_buttons = [
        [InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}")]
    ]
    
    # Username bo'lsa xavfsiz tugma qo'shamiz
    if callback.from_user.username:
        inline_buttons[0].append(
            InlineKeyboardButton(text="👤 Profili", url=f"https://t.me/{callback.from_user.username}")
        )

    admin_inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    # -------------------------------------------------------------
    
    # Adminlar + Owner
    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)
    
    for recipient_id in recipients:
        try:
            await bot.send_message(
                chat_id=recipient_id, 
                text=admin_msg, 
                parse_mode="HTML", 
                reply_markup=admin_inline_kb,
                disable_web_page_preview=True
            )
            print(f"✅ Feedback adminga bordi: {recipient_id}")
        except Exception as e:
            print(f"❌ Admin {recipient_id} ga yuborishda xatolik: {e}")

# 5. JAVOB BERISH TUGMASI (ADMIN UCHUN)
@router.callback_query(F.data.startswith("reply:"))
async def handle_reply_callback(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target_user_id=target_id)
    await call.message.answer(f"✍️ Foydalanuvchiga (ID: {target_id}) yubormoqchi bo'lgan javobingizni yozing:")
    await state.set_state(ReplyState.waiting_for_reply)
    await call.answer()

# 6. JAVOB XABARINI YUBORISH
@router.message(ReplyState.waiting_for_reply)
async def send_reply_to_user(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_id = data.get("target_user_id")
    await state.clear()
    
    try:
        await bot.send_message(
            chat_id=target_id,
            text=f"✉️ **Administratsiyadan javob:**\n\n{message.text}",
            parse_mode="Markdown"
        )
        await message.answer("✅ Javobingiz muvaffaqiyatli yetkazildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yetkazishda xatolik: {e}")"""



from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import get_teachers_keyboard, get_star_rating_keyboard
from states.states import FeedbackRatingState, ReplyState

router = Router()

OWNER_ID = 1299498580  

@router.message(F.text == "✍️ O'qituvchilarni baholash va fikr bildirish")
async def start_rating_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "O'zingizning yoki farzandingizning o'qituvchisini tanlang:",
        reply_markup=get_teachers_keyboard()
    )

@router.callback_query(F.data.startswith("select_teacher:"))
async def teacher_selected(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(selected_teacher=teacher_name)
    await state.set_state(FeedbackRatingState.waiting_for_comment)
    
    await callback.message.edit_text(
        f"Siz **{teacher_name}**ni tanladingiz.\n\n"
        f"Iltimos, o'qituvchi haqida o'z fikringiz va mulohazalaringizni yozib yuboring:",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(FeedbackRatingState.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)
    await state.set_state(FeedbackRatingState.waiting_for_rating)
    
    await message.answer(
        "Rahmat! Endi o'qituvchini 1 dan 5 gacha bo'lgan yulduzli reyting bilan baholang:",
        reply_markup=get_star_rating_keyboard()
    )

@router.callback_query(FeedbackRatingState.waiting_for_rating, F.data.startswith("star:"))
async def rating_received(callback: CallbackQuery, state: FSMContext, bot: Bot):
    rating_val = int(callback.data.split(":")[1])
    
    data = await state.get_data()
    teacher_name = data.get("selected_teacher")
    comment_text = data.get("comment_text", "Fikr bildirilmagan")
    
    if not teacher_name:
        await callback.answer("⚠️ Qaytadan o'qituvchini tanlab urinib ko'ring.", show_alert=True)
        await state.clear()
        return

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name or "Foydalanuvchi"

    await db.save_teacher_rating(user_id, teacher_name, rating_val, comment_text)
    await state.clear()
    
    stars_display = "⭐" * rating_val

    await callback.message.edit_text(
        f"✅ **Bahoyingiz qabul qilindi!**\n\n"
        f"👨‍🏫 O'qituvchi: **{teacher_name}**\n"
        f"⭐ Baho: **{stars_display} ({rating_val}/5)**\n"
        f"💬 Fikringiz: _{comment_text}_\n\n"
        f"E'tiboringiz uchun tashakkur!",
        parse_mode="Markdown"
    )
    await callback.answer("Bahoyingiz saqlandi!")

    if callback.from_user.username:
        user_link_html = f"<a href='https://t.me/{callback.from_user.username}'>{user_name}</a>"
        profile_btn = InlineKeyboardButton(
            text="👤 Profili", 
            url=f"https://t.me/{callback.from_user.username}"
        )
    else:
        user_link_html = f"<b>{user_name}</b>"
        profile_btn = InlineKeyboardButton(
            text="👤 Profili", 
            callback_data=f"show_profile:{user_id}"
        )

    admin_msg = (
        f"📩 <b>Yangi fikr/taklif (#ID_{user_id}):</b>\n\n"
        f"👨‍🏫 <b>O'qituvchi:</b> {teacher_name}\n"
        f"⭐ <b>Baho:</b> {stars_display} ({rating_val}/5)\n"
        f"💬 <b>Fikr:</b> {comment_text}\n\n"
        f"👤 <b>Yuboruvchi:</b> {user_link_html}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>"
    )

    inline_buttons = [
        [
            InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply:{user_id}"),
            profile_btn
        ]
    ]

    admin_inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    
    db_admins = await db.get_all_admins() or []
    recipients = set(db_admins)
    recipients.add(OWNER_ID)
    
    for recipient_id in recipients:
        try:
            await bot.send_message(
                chat_id=recipient_id, 
                text=admin_msg, 
                parse_mode="HTML", 
                reply_markup=admin_inline_kb,
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"❌ Admin {recipient_id} ga yuborishda xatolik: {e}")

@router.callback_query(F.data.startswith("reply:"))
async def handle_reply_callback(call: CallbackQuery, state: FSMContext):
    target_id = int(call.data.split(":")[1])
    await state.update_data(target_user_id=target_id)
    await call.message.answer(f"✍️ Foydalanuvchiga (ID: {target_id}) yubormoqchi bo'lgan javobingizni yozing:")
    await state.set_state(ReplyState.waiting_for_reply)
    await call.answer()

@router.message(ReplyState.waiting_for_reply)
async def send_reply_to_user(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_id = data.get("target_user_id")
    await state.clear()
    
    try:
        await bot.send_message(
            chat_id=target_id,
            text=f"✉️ **Administratsiyadan javob:**\n\n{message.text}",
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