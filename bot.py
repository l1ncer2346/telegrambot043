import telebot as tb
import COVID19Py
import requests
import config
from telebot import types

bot = tb.TeleBot(config.token)
virus = COVID19Py.COVID19()

@bot.message_handler(commands = ['start'])
def Welcome(message):
	sticker = open('media/welcome.tgs', 'rb')
	bot.send_sticker(message.chat.id, sticker)
	sticker.close()
	reply = 'Welcome <b>{0}</b>! \n I`m <i>{1.first_name} bot</i> \n Use basic commands to get some information about corona virus'.format(message.from_user.first_name, bot.get_me())
	bot.send_message(message.chat.id, reply, parse_mode = 'html')

@bot.message_handler(commands = ['get_last_inf_in_world'])
def get_info_about_cv_in_wrld(message):
	resulted = virus.getLatest()
	bot.send_message(message.chat.id, 'Situation in world : Confirmed - {0}, Deaths - {1}'.format(resulted['confirmed'], resulted['deaths']))

@bot.message_handler(commands = ['get_last_inf_in_country'])
def get_info_about_cv_in_cntr(message):
	markup = types.InlineKeyboardMarkup(row_width = 8)
	item0 = types.InlineKeyboardButton('Россия', callback_data = 'ru')
	item1 = types.InlineKeyboardButton('Англия', callback_data = 'gb')
	item2 = types.InlineKeyboardButton('Сша', callback_data = 'us')
	item3 = types.InlineKeyboardButton('Италия', callback_data = 'it')
	item4 = types.InlineKeyboardButton('Испания', callback_data = 'es')
	item5 = types.InlineKeyboardButton('Германия', callback_data = 'de')
	item6 = types.InlineKeyboardButton('Франция', callback_data = 'fr')
	item7 = types.InlineKeyboardButton('Китай', callback_data = 'cn')
	markup.add(item0, item1, item2, item3, item4, item5, item6, item7)
	bot.send_message(message.chat.id, 'Choose country:', reply_markup = markup)

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
	if call.message:
		result_c = virus.getLocationByCountryCode(call.data)
		bot.send_message(call.message.chat.id, '{0} : Confirmed - {1}, Deaths - {2}'.format(result_c[0]['country'], result_c[0]['latest']['confirmed'], result_c[0]['latest']['deaths']))
		bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Choose country:', reply_markup = None)
		sticker = open('media/stay_home.tgs', 'rb')
		bot.send_sticker(call.message.chat.id, sticker)
		sticker.close()

@bot.message_handler(commands = ['why_is_fcv'])
def get_name_reason(message):
	bot.send_message(message.chat.id, '<em>FCV does mean "Fuck Corona Virus!"</em>', parse_mode = 'html')
	sticker = open('media/nb.tgs', 'rb')
	bot.send_sticker(message.chat.id, sticker)
	sticker.close()

@bot.message_handler(content_types = ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def warning(message):
	bot.send_message(message.chat.id, '<b>I don`t understand your messages.</b><i> Use the basic commands which first simbol is</i> /', parse_mode = 'html')

bot.polling(none_stop=True)