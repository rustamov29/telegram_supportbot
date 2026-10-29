"""# keyboards/default.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(role: str) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="✍️ Fikr va taklif bildirish")],
        [KeyboardButton(text="📞 Biz bilan aloqa")]
    ]
    if role in ['owner', 'admin']:
        buttons.append([KeyboardButton(text="⚙️ Admin Panel")])
        
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_admin_keyboard(role: str) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="📊 Bot statistikasi"), KeyboardButton(text="📢 Xabar yuborish (Broadcast)")],
    ]
    if role == 'owner':
        buttons.append([KeyboardButton(text="➕ Admin qo'shish"), KeyboardButton(text="➖ Adminni olib tashlash")])
        buttons.append([KeyboardButton(text="👑 Egalikni o'tkazish")])
    buttons.append([KeyboardButton(text="⬅️ Bosh menyuga qaytish")])
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)"""








# keyboards/default.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(role: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="✍️ O'qituvchilarni baholash va fikr bildirish")],
        [KeyboardButton(text="📞 Biz bilan aloqa")]
    ]
    if role in ['admin', 'owner']:
        keyboard.append([KeyboardButton(text="⚙️ Admin Panel")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_admin_keyboard(role: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📊 O'qituvchilar statistikasi")],
        [KeyboardButton(text="📈 Foydalanuvchilar statistikasi")],
        [KeyboardButton(text="📢 Xabar yuborish (Broadcast)")]
    ]
    if role == 'owner':
        keyboard.append([KeyboardButton(text="➕ Admin qo'shish"), KeyboardButton(text="➖ Adminni olib tashlash")])
    
    keyboard.append([KeyboardButton(text="⬅️ Bosh menyuga qaytish")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)





