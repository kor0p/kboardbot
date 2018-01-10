
#-*- coding:utf-8 -*-
import telebot as tb
from telebot.types import *

id_=0 ; t='\'' ; b='{}' 

eng='`qwertyuiop[]asdfghjkl;'+t+'zxcvbnm,./~#&|QWERTYUIOP'+b+'ASDFGHJKL:"ZXCVBNM<>?'

ukr='ёйцукенгшщзхїфівапролджєячсмитьбю.Ё№?/ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,'

bot = tb.TeleBot('454578455:AAFSP0yk7hBVZE26gI9v-Qeu6Jpi2wrIfJA')

'''
a=input('Input smthg id 1:')
b=input('Input smthg id 2:')
c=input('Input smthg text:')

bot.send_message(
		a,
		'Єєєє, це тест бот! '+str(b)+' : '+c)
'''
def translit(t,ar1=eng,ar2=ukr):
	for i in range(len(t)):
		if t[i] in ar1:
			index=ar1.index(t[i])
			t=t[:i]+ar2[index]+t[i+1:]
		else:
			pass
	return t
'''
ffff= 1001192221824*(-1)
'''
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

	id_+=1  ;  q=query.query

	results = [' ',]  ;  title=''

	if q[-1]=='!':
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
