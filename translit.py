
#-*- coding:utf-8 -*-
import telebot
from config import token

eng = list('`qwertyuiop[]asdfghjkl;\'zxcvbnm,./~#&|QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?')
ukr = list('ёйцукенгшщзхїфівапролджєячсмитьбю.Ё№?/ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,')

bot = telebot.TeleBot(token)

back_sign = '~'

def translit(input_text, language_1 = eng,language_2 = ukr):
	text = list(input_text)
	for char_index in range(len(text)):
		if text[char_index] in language_1:
			text[char_index] = language_2[language_1.index(text[char_index])]
	return ''.join(text)

@bot.message_handler(commands=['start','help'])
def message(m):
	bot.send_message(m.from_user.id,
		"""
		Введіть текст на англійській розкладці, будь ласка !
		Input text in English keyboard layout, please

		Використовуйте ~ в кінці, щоб змінити розкладку назад
		Use ~ in the end to get backward changes
		""")

@bot.message_handler(content_types=['text'])
def message(m):
	if m.text[-1]==back_sign:
		text=translit(m.text[:-1],ukr,eng)
	else:
		text=translit(m.text)
	bot.send_message(m.chat.id,text)

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
	text = query.query
	if text[-1]==back_sign:
		title = translit(text[:-1],ukr,eng)
	else:
		title = translit(text)
	output_text = title
	result = telebot.types.InlineQueryResultArticle(
		id=query.id,
		title=title,
		input_message_content=telebot.types.\
		InputTextMessageContent(message_text=output_text),
		)

	bot.answer_inline_query(query.id,[result])


if __name__ == '__main__':
	bot.polling(none_stop=True)
