import telebot
from main import recognize_text
bot = telebot.TeleBot('Ваш токен')

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    change_langs = telebot.types.InlineKeyboardButton('Изменить распозноваемые языки', callback_data='change_langs')
    sent_photo = telebot.types.InlineKeyboardButton('Прислать фото для распозновния', callback_data='send_photo')
    keyboard.add(sent_photo, change_langs)
    bot.send_message(message.chat.id, 'Привет! Пришли мне картинку, а в ответ получишь текст с пикчи', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def call_check(call):
    if call.data == 'change_langs':
        bot.send_message(call.message.chat.id, "Пришли мне список используемых языков в таком формате:\n en ru\n Без кавычек, через пробел"
                                               "По дефолту уже установлен английсий, так же важно:"
                                               "Языки разных групп нельзя использовать вместе. Например китайский с русским и немецким. Такие языки можно использовать только с английским")
    elif call.data == 'Пришли фото для распозновния':
        bot.send_message(call.message.chat.id, 'send me photo')

langs = 'en'
@bot.message_handler(content_types=['text'])
def change_langs(message):
    global langs
    langs = ''
    langs = message.text.lower().split(' ')
    bot.send_message(message.chat.id, 'Отлично! Теперь пришли фото для распозновния')

@bot.message_handler(content_types=['photo'])
def text_from_photo(message):
    info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    down_f = bot.download_file(info.file_path)

    scr = 'pics/'+info.file_path
    with open(scr, 'wb') as new_file:
        new_file.write(down_f)

    bot.send_message(message.chat.id, 'Пожалуйтса, ожидайте. Если на картинке присутствует много текста, то процесс может занять время.')

    full_text, pic_path = recognize_text(info.file_path, langs)

    bot.send_message(message.chat.id, full_text)

    image = open(pic_path, 'rb')
    bot.send_photo(message.chat.id, image)


bot.polling()
