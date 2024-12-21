from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура выбора сектора
def get_sector_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    sectors = ["A", "B", "C", "D", "E", "F", "G", "H"]
    buttons = [KeyboardButton(sector) for sector in sectors]
    markup.add(*buttons)
    return markup


# Основная клавиатура для пользователя
def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Оставить заявку"))
    return markup


# Кнопка для администратора для пометки заявки как решённой
def get_admin_markup(request_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Пометить как решённую", callback_data=f"resolve_{request_id}")
    )
    return markup
