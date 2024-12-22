import telebot
from telebot.types import ReplyKeyboardRemove
import sqlite3
from keyboard import get_sector_keyboard, get_main_keyboard, get_admin_markup

TOKEN = "7630583007:AAGvDmu3Be00Gcn0TI7_KAmbX8d3nMYInHQ"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = -1002343745365

# Создание базы данных
conn = sqlite3.connect("requests.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    sector TEXT,
    comment TEXT,
    status TEXT DEFAULT 'В обработке'
)
""")
conn.commit()


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Нажми на кнопку, чтобы оставить заявку.",
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "Оставить заявку")
def request_info(message):
    bot.send_message(
        message.chat.id,
        "Выберите сектор из предложенных:",
        reply_markup=get_sector_keyboard()
    )
    bot.register_next_step_handler(message, get_sector)


def get_sector(message):
    sector = message.text
    bot.send_message(
        message.chat.id,
        "Теперь добавьте комментарий:",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, get_comment, sector)


def get_comment(message, sector):
    comment = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    cursor.execute("""
        INSERT INTO requests (user_id, username, sector, comment)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, sector, comment))
    conn.commit()

    request_id = cursor.lastrowid

    full_message = (
        f"🔔 Новая заявка #{request_id}!\n\n"
        f"📍 Сектор: {sector}\n"
        f"📝 Комментарий: {comment}\n"
        f"👤 Пользователь: @{username if username else 'Без имени'}"
    )
    bot.send_message(ADMIN_ID, full_message, reply_markup=get_admin_markup(request_id))

    # Уведомление пользователя
    bot.send_message(message.chat.id,
                     "Заявка отправлена администратору. Спасибо!",
                     reply_markup=get_main_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("resolve_"))
def resolve_request(call):
    request_id = int(call.data.split("_")[1])

    cursor.execute("""
        UPDATE requests
        SET status = 'Решена'
        WHERE id = ?
    """, (request_id,))
    conn.commit()

    bot.answer_callback_query(call.id, "Заявка помечена как решённая.")
    bot.edit_message_text(
        f"Заявка #{request_id} была решена.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    cursor.execute("SELECT user_id FROM requests WHERE id = ?", (request_id,))
    user_id = cursor.fetchone()[0]
    bot.send_message(user_id, f"Ваша заявка #{request_id} была решена. Спасибо за ожидание!")


@bot.message_handler(commands=['history'])
def show_history(message):
    if message.chat.id == ADMIN_ID:
        cursor.execute("SELECT id, sector, comment, status FROM requests")
        requests = cursor.fetchall()

        if requests:
            history = "\n".join([
                f"#{req[0]} | Сектор: {req[1]} | Комментарий: {req[2]} | Статус: {req[3]}"
                for req in requests
            ])
            bot.send_message(ADMIN_ID, f"История заявок:\n\n{history}")
        else:
            bot.send_message(ADMIN_ID, "История заявок пуста.")
    else:
        bot.send_message(message.chat.id, "Эта команда доступна только администратору.")


bot.polling()
