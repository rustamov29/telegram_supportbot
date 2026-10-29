"""# states/states.py
from aiogram.fsm.state import State, StatesGroup

class FeedbackState(StatesGroup):
    waiting_for_text = State()

class ReplyState(StatesGroup):
    waiting_for_reply = State()
    target_user_id = State()

class AdminState(StatesGroup):
    waiting_for_add_admin = State()
    waiting_for_remove_admin = State()
    waiting_for_new_owner = State()
    waiting_for_broadcast = State()

"""




# states/states.py
from aiogram.fsm.state import State, StatesGroup

class FeedbackRatingState(StatesGroup):
    waiting_for_comment = State()
    waiting_for_rating = State()

class FeedbackState(StatesGroup):
    waiting_for_text = State()

class AdminState(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_add_admin = State()
    waiting_for_remove_admin = State()

class ReplyState(StatesGroup):
    waiting_for_reply = State()

