
#-*- coding:utf-8 -*-
import telebot as tb
from telebot.types import *
from config import token
id_=0

eng='`qwertyuiop[]asdfghjkl;\'zxcvbnm,./~#&|QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'

ukr='ёйцукенгшщзхїфівапролджєячсмитьбю.Ё№?/ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,'

bot = tb.TeleBot(token)

def translit(t,ar1=eng,ar2=ukr):
	for i in range(len(t)):
		if t[i] in ar1:
			index=ar1.index(t[i])
			t=t[:i]+ar2[index]+t[i+1:]
	return t

@bot.message_handler(commands=['start','help'])
def message(m):
	bot.send_message(m.from_user.id,
		'Введіть текст на англійській розкладці, будь ласка !')

@bot.message_handler(content_types=['text'])
def message(m):
	if m.text[-1]=='!':
		text=translit(m.text[:-1],ukr,eng)
	else:
		text=translit(m.text)
	bot.send_message(m.chat.id,text)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
	global id_

	id_+=1
	q=query.query
	results = [' ',]
	title=''
	
	if q[-1]=='~':
		temp=translit(q[:-1],ukr,eng)
	else:
		temp=translit(q)
	
	title+=temp
	text=title
	single_msg = InlineQueryResultArticle(
		id=id_,
		title=title,
		input_message_content=InputTextMessageContent(message_text=text),
		)
	results.append(single_msg)

	bot.answer_inline_query(query.id,results)


if __name__ == '__main__':
	bot.polling(none_stop=True)
