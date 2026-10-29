"""# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_feedback_inline(user_id: int) -> InlineKeyboardMarkup:
    user_link = f"tg://user?id={user_id}"
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply_{user_id}"),
        InlineKeyboardButton(text="👤 Profili", url=user_link)
    ]])"""






"""# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_teachers_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🏫 Ibrohim teacher", callback_data="select_teacher:Ibrohim teacher")],
        [InlineKeyboardButton(text="👨‍🏫 Yaxyo teacher", callback_data="select_teacher:Yaxyo teacher")],
        [InlineKeyboardButton(text="👨‍🏫 Muhammad teacher", callback_data="select_teacher:Muhammad teacher")],
        [InlineKeyboardButton(text="👩‍🏫 Gulchehra teacher", callback_data="select_teacher:Gulchehra teacher")]
    ])

def get_star_rating_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 ⭐️", callback_data="rate_star:1"),
            InlineKeyboardButton(text="2 ⭐️", callback_data="rate_star:2"),
            InlineKeyboardButton(text="3 ⭐️", callback_data="rate_star:3"),
            InlineKeyboardButton(text="4 ⭐️", callback_data="rate_star:4"),
            InlineKeyboardButton(text="5 ⭐️", callback_data="rate_star:5")
        ]
    ])"""




from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_teachers_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🏫 Ibrohim teacher", callback_data="select_teacher:Ibrohim teacher")],
        [InlineKeyboardButton(text="👨‍🏫 Yaxyo teacher", callback_data="select_teacher:Yaxyo teacher")],
        [InlineKeyboardButton(text="👨‍🏫 Muhammad teacher", callback_data="select_teacher:Muhammad teacher")],
        [InlineKeyboardButton(text="👩‍🏫 Gulchehra teacher", callback_data="select_teacher:Gulchehra teacher")]
    ])

def get_star_rating_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 ⭐️", callback_data="star:1"),
            InlineKeyboardButton(text="2 ⭐️", callback_data="star:2"),
            InlineKeyboardButton(text="3 ⭐️", callback_data="star:3"),
            InlineKeyboardButton(text="4 ⭐️", callback_data="star:4"),
            InlineKeyboardButton(text="5 ⭐️", callback_data="star:5")
        ]
    ])