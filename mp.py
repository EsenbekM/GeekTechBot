from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cl = InlineKeyboardMarkup(row_width=2)
yes = InlineKeyboardButton(text="YES", callback_data="yes")
no = InlineKeyboardButton(text="NO", callback_data="no")

cl.insert(yes)
cl.insert(no)