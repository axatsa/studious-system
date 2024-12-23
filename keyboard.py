from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура выбора сектора
def get_sector_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    sectors = ["A", "B", "C", "D", "E", "F", "G", "H"]
    buttons = [KeyboardButton(sector) for sector in sectors]
    markup.add(*buttons)
    return markup


def get_reason_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    problems = ['Cлетел проектор', 'WiFi не работает', 'Не грузит презентация', 'Петличка села', 'Нужен крликер',
                'Доска грязная', 'Нужен марер', 'Лист посещаемости нужно', "Не хватает мест в секторе", 'Нужен Админ',
                'Перемена', 'Нужна зарядка для ноутбука', 'Нужен ноутбук', 'В секторе холодно', 'В секторе жарко',
                'Звука нет в YouTube', 'Звука нет в StreamYard', 'Проектор мутный', 'Нужен переходник HDMI',
                'Нужен переходник USB']
    buttons = [KeyboardButton(problem) for problem in problems]
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
