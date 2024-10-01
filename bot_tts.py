from telebot import TeleBot
from config_tts import TOKEN, MAX_SYMBOLS, MAX_SYMBOLS_PER_USER
from telebot.types import Message, ReplyKeyboardMarkup
from db_tts import count_all_symbol, insert_row, prepare_db, newdata
from info_tts import start_message, help_message
from speechkit_stt import text_to_speech

bot = TeleBot(TOKEN)

def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start'])
def bot_start(message):
    keyboard = create_keyboard(["/help"])
    bot.send_message(message.chat.id, text=start_message, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def bot_help(message):
    keyboard = create_keyboard(["/start", "/help", "/tts"])
    bot.send_message(chat_id=message.chat.id, text=help_message, reply_markup=keyboard)


@bot.message_handler(commands=['tts'])
def tts(message: Message):
    bot.send_message(message.chat.id, "Введите текст: ")
    bot.register_next_step_handler(message, tts2)

def tts2(message: Message):
    user_id = message.chat.id
    text = message.text

    insert_row(user_id, text, len(text))

    if message.content_type != 'text':
        bot.send_message(message.chat.id, "Отправьте текст")
        bot.register_next_step_handler(message, tts2)
        return

    if len(message.text) >= MAX_SYMBOLS:
        bot.send_message(message.chat.id, "Слишком много симбоблс")
        bot.register_next_step_handler(message, tts2)
        return

    if count_all_symbol(message.chat.id) >= MAX_SYMBOLS_PER_USER:
        bot.send_message(message.chat.id, "Слишком много симбоблс")
        return

    status, message_data = text_to_speech(text)
    if not status:
        bot.send_message(message.chat.id, message_data)
        return

    bot.send_voice(message.chat.id, message_data)

if __name__ == '__main__':
    prepare_db()
    bot.infinity_polling()