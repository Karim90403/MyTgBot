import telebot
import config
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
 
@bot.message_handler(commands=['start'])
def welcome(message):
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Дни без ссор 📅")
    item2 = types.KeyboardButton("Милые списочки 💗")
 
    markup.add(item1, item2)
 
    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы можно быть милашкой😘".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
 
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Милые списочки 💗":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Настя🐰", callback_data='Anastasia')
            item2 = types.InlineKeyboardButton("Карим", callback_data='Karim')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Чей список хочешь посмотреть?', reply_markup=markup)

        elif message.text == "Дни без ссор 📅":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Угу(", callback_data='bad')
            item2 = types.InlineKeyboardButton("👉🏻👈🏻", callback_data='soso')
            item3 = types.InlineKeyboardButton("Не-а!", callback_data='good')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Поссорились?', reply_markup=markup)

        else:
            if message.from_user.username == 'karim_muzafarov':
                config.Anastasia_list.append(message.text)
                bot.reply_to(message, "Отлично, тепрь это в списке милостей Насти 😊")
            elif message.from_user.username == 'They_ask_me':
                config.Karim_list.append(message.text)
                bot.reply_to(message, "Отлично, тепрь это в списке милостей Карима 😊")
            else:
                bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
                config.days_without += 1
                bot.send_message(call.message.chat.id, config.days_without)
            elif call.data == 'soso':
                bot.send_message(call.message.chat.id, 'Ну и нейтральненько...')
                bot.send_message(call.message.chat.id, config.days_without)
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
                config.days_without = 0
                bot.send_message(call.message.chat.id, config.days_without)
            elif call.data == 'Anastasia':
                bot.send_message(call.message.chat.id, "Списочек Насти🥰")
                for i in config.Anastasia_list:
                    bot.send_message(call.message.chat.id, i)
            elif call.data == 'Karim':
                bot.send_message(call.message.chat.id, "Списочек Карима🥰")
                for i in config.Karim_list:
                    bot.send_message(call.message.chat.id, i)
                
 
    except Exception as e:
        print(repr(e))
 
# RUN
bot.polling(none_stop=True)