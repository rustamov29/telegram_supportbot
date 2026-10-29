"""# handlers/admin.py
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import database as db
from states.states import AdminState
from keyboards.default import get_admin_keyboard

router = Router()

@router.message(F.text == "⚙️ Admin Panel")
async def admin_panel(message: Message):
    role = await db.get_user_role(message.from_user.id)
    if role not in ['owner', 'admin']:
        return

    text = f"⚙️ **Admin Panelga xush kelibsiz!**\nSizning rolingiz: **{role.upper()}**\nKerakli bo'limni tanlang:"
    markup = get_admin_keyboard(role)
    await message.answer(text, reply_markup=markup, parse_mode="Markdown")

@router.message(F.text == "📊 Bot statistikasi")
async def show_stats(message: Message):
    role = await db.get_user_role(message.from_user.id)
    if role not in ['owner', 'admin']:
        return
        
    total_users, total_admins, total_feedbacks = await db.get_stats()
    stats_text = (
        "📊 **BOT STATISTIKASI:**\n\n"
        f"👥 **Jami obunachilar:** {total_users} ta\n"
        f"🛠 **Adminlar soni:** {total_admins} ta\n"
        f"💬 **Kelib tushgan fikrlar:** {total_feedbacks} ta"
    )
    await message.answer(stats_text, parse_mode="Markdown")

@router.message(F.text == "📢 Xabar yuborish (Broadcast)")
async def start_broadcast(message: Message, state: FSMContext):
    role = await db.get_user_role(message.from_user.id)
    if role not in ['owner', 'admin']:
        return
    await message.answer("Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:")
    await state.set_state(AdminState.waiting_for_broadcast)

@router.message(AdminState.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    users = await db.get_all_users()
    count = 0
    await message.answer("📢 Xabarni yuborish boshlandi...")
    
    for u_id in users:
        try:
            await bot.copy_message(chat_id=u_id, from_chat_id=message.chat.id, message_id=message.message_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
            
    await message.answer(f"✅ Xabar muvaffaqiyatli {count} ta foydalanuvchiga yetkazildi!")

@router.message(F.text == "➕ Admin qo'shish")
async def add_admin_start(message: Message, state: FSMContext):
    if await db.get_user_role(message.from_user.id) != 'owner':
        return
    await message.answer("Yangi admin qilmoqchi bo'lgan foydalanuvchining **Telegram ID** sini kiriting:")
    await state.set_state(AdminState.waiting_for_add_admin)

@router.message(AdminState.waiting_for_add_admin)
async def add_admin_finish(message: Message, state: FSMContext):
    try:
        new_id = int(message.text)
        await db.set_user_role(new_id, 'admin')
        await state.clear()
        await message.answer(f"✅ ID `{new_id}` muvaffaqiyatli **Admin** qilindi!", parse_mode="Markdown")
    except ValueError:
        await message.answer("Iltimos, to'g'ri ID raqam kiriting.")

@router.message(F.text == "➖ Adminni olib tashlash")
async def remove_admin_start(message: Message, state: FSMContext):
    if await db.get_user_role(message.from_user.id) != 'owner':
        return
    await message.answer("Adminlikdan olmoqchi bo'lgan foydalanuvchining **Telegram ID** sini kiriting:")
    await state.set_state(AdminState.waiting_for_remove_admin)

@router.message(AdminState.waiting_for_remove_admin)
async def remove_admin_finish(message: Message, state: FSMContext):
    try:
        rem_id = int(message.text)
        await db.set_user_role(rem_id, 'user')
        await state.clear()
        await message.answer(f"✅ ID `{rem_id}` adminlikdan olindi.", parse_mode="Markdown")
    except ValueError:
        await message.answer("Iltimos, to'g'ri ID raqam kiriting.")

@router.message(F.text == "👑 Egalikni o'tkazish")
async def transfer_start(message: Message, state: FSMContext):
    if await db.get_user_role(message.from_user.id) != 'owner':
        return
    await message.answer("⚠️ **DIQQAT!** Egalikni o'tkazmoqchi bo'lgan yangi eganing **Telegram ID** sini yuboring:")
    await state.set_state(AdminState.waiting_for_new_owner)

@router.message(AdminState.waiting_for_new_owner)
async def transfer_finish(message: Message, state: FSMContext):
    try:
        new_owner_id = int(message.text)
        await db.transfer_ownership(message.from_user.id, new_owner_id)
        await state.clear()
        await message.answer(f"🎉 Egalik muvaffaqiyatli ID `{new_owner_id}` ga o'tkazildi!", parse_mode="Markdown")
    except ValueError:
        await message.answer("Iltimos, to'g'ri Telegram ID kiriting.")"""





# handlers/admin.py
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.default import get_admin_keyboard, get_main_keyboard
from states.states import AdminState

router = Router()

# Admin panel bosh menyusi (Faqat admin va owner kira oladi)
@router.message(F.text == "⚙️ Admin Panel")
async def admin_panel(message: Message):
    role = await db.get_user_role(message.from_user.id)
    if role in ['admin', 'owner']:
        await message.answer("🛠 **Admin paneliga xush kelibsiz:**", reply_markup=get_admin_keyboard(role), parse_mode="Markdown")
    else:
        await message.answer("❌ Sizda bu bo'limga kirish huquqi yo'q.")

# O'qituvchilar statistikasi handleri:

@router.message(F.text == "📊 O'qituvchilar statistikasi")
async def show_teacher_stats(message: Message):
    teachers = ["Ibrohim teacher", "Yaxyo teacher", "Muhammad teacher", "Gulchehra teacher"]
    
    msg_text = "📊 **O'qituvchilarning umumiy reyting statistikasi:**\n\n"
    
    for teacher in teachers:
        avg_rating, count = await db.get_teacher_stats(teacher)
        
        if count > 0:
            # 1. Bahoni 1 ta o'nlik kasrgacha yaxlitlaymiz (masalan: 3.3, 4.5)
            rating_val = round(avg_rating, 1)
            
            # 2. Yulduzchalarni eng yaqin butun songa qarab chiqarish
            stars_count = round(rating_val)
            stars_display = "⭐" * stars_count
            
            # 3. Aynan shu yerda matn shakllantiriladi
            msg_text += (
                f"👨‍🏫 **{teacher}**\n"
                f"├ O'rtacha baho: **{rating_val:.1f} / 5** {stars_display}\n"
                f"└ Jami fikrlar/ovozlar: **{count} ta**\n\n"
            )
        else:
            msg_text += f"👨‍🏫 **{teacher}**\n└ Hali baholanmagan ⚪\n\n"
            
    await message.answer(msg_text, parse_mode="Markdown")

# 2. BOT STATISTIKASI (2-rasmdagidek to'liq ko'rinishda)
@router.message(F.text == "📈 Foydalanuvchilar statistikasi")
async def user_stats(message: Message):
    role = await db.get_user_role(message.from_user.id)
    if role in ['admin', 'owner']:
        users_count = await db.get_user_count()
        admins_count = await db.get_admin_count()
        feedback_count = await db.get_total_feedback_count()
        
        stat_msg = (
            "📊 **BOT STATISTIKASI:**\n\n"
            f"👥 **Jami obunachilar:** {users_count} ta\n"
            f"🛠 **Adminlar soni:** {admins_count} ta\n"
            f"💬 **Kelib tushgan fikrlar:** {feedback_count} ta"
        )
        
        await message.answer(stat_msg, parse_mode="Markdown")

# 3. BROADCAST
@router.message(F.text == "📢 Xabar yuborish (Broadcast)")
async def broadcast_start(message: Message, state: FSMContext):
    role = await db.get_user_role(message.from_user.id)
    if role in ['admin', 'owner']:
        await message.answer("Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:")
        await state.set_state(AdminState.waiting_for_broadcast)

@router.message(AdminState.waiting_for_broadcast)
async def broadcast_process(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    users = await db.get_all_users()
    success, failed = 0, 0
    
    await message.answer("⏳ Xabar yuborish boshlandi...")
    for uid in users:
        try:
            await bot.send_message(uid, message.text)
            success += 1
        except Exception:
            failed += 1

    await message.answer(f"✅ Broadcast yakunlandi!\n\n Muvaffaqiyatli: {success} ta\n Yetib bormadi: {failed} ta")

# 4. ADMIN QO'SHISH (Faqat owner uchun)
@router.message(F.text == "➕ Admin qo'shish")
async def add_admin_start(message: Message, state: FSMContext):
    role = await db.get_user_role(message.from_user.id)
    if role == 'owner':
        await message.answer("Yangi adminning Telegram ID raqamini kiriting:")
        await state.set_state(AdminState.waiting_for_add_admin)

@router.message(AdminState.waiting_for_add_admin)
async def add_admin_process(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqamlardan iborat Telegram ID kiriting.")
        return
    
    new_admin_id = int(message.text)
    await db.set_user_role(new_admin_id, 'admin')
    await state.clear()
    await message.answer(f"✅ ID: **{new_admin_id}** muvaffaqiyatli admin qilindi!", parse_mode="Markdown")

# 5. ADMINNI OLIB TASHLASH (Faqat owner uchun)
@router.message(F.text == "➖ Adminni olib tashlash")
async def remove_admin_start(message: Message, state: FSMContext):
    role = await db.get_user_role(message.from_user.id)
    if role == 'owner':
        await message.answer("Olib tashlanadigan adminning Telegram ID raqamini kiriting:")
        await state.set_state(AdminState.waiting_for_remove_admin)

@router.message(AdminState.waiting_for_remove_admin)
async def remove_admin_process(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqamlardan iborat Telegram ID kiriting.")
        return
    
    admin_id = int(message.text)
    await db.set_user_role(admin_id, 'user')
    await state.clear()
    await message.answer(f"✅ ID: **{admin_id}** adminlikdan olib tashlandi!", parse_mode="Markdown")






