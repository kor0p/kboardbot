
#-*- coding:utf-8 -*-
import telebot
from telebot import types
from config import token
from random import choice
random_list = (choice((0,)*(20-1)+(1,)) for i in range(100000))

bot = telebot.TeleBot(token)


class Layout:
    def __init__(self, name, value, have_big_letters=True):
        self.name = name
        self.big = have_big_letters
        value = value.replace('\n', '').replace('    ', '')
        self.value = value[:96]
        self.spec = value[96:]
        if not self.spec:
            self.spec = self.value
        #self.main = self.value[13:48]+self.spec[13:48]

    def __repr__(self):
        return self.value+self.spec

    __str__ = __repr__

    def __len__(self):
        return len(str(self))

    def __getitem__(self, key):
        return str(self)[key]

    def index(self, char):
        return str(self).index(char)

    def translit(self, another, text):
        assert isinstance(another, Layout)
        if not another.big:
            text = text.lower()
        output_text = ''.join([
            another[self.index(char)]
            if char in self else
            char
            for char in text
        ])
        if not self.big:
            output_text = output_text.lower()
        return output_text


layouts = {
    'eng': Layout('English🇬🇧',
                  """
    `1234567890-=
    qwertyuiop[]
    asdfghjkl;'\\
    \\zxcvbnm,./

    ~!@#$%^&*()_+
    QWERTYUIOP{}
    ASDFGHJKL:\"|
    |ZXCVBNM<>?
    """),
    'ukr': Layout('Ukrainian🇺🇦',
                  """
    `1234567890-=
    йцукенгшщзхї
    фівапролджєґ
    /ячсмитьбю.

    ~!"№;%:?*()_+
    ЙЦУКЕНГШЩЗХЇ
    ФІВАПРОЛДЖЄҐ
    |ЯЧСМИТЬБЮ,

    ́¹²§$°<>•[]—≠
    йцў®ёнгшщзхъ
    фывапролджэ\
    /яч©ми™ь«»/

    ~!’₴€%:?*{}–±
    ЙЦЎКЁНГШЩЗХЪ
    ФЫВАПРОЛДЖЭ|
    |ЯЧСМИТЬ„“…
    """),
    'rus': Layout('Russian🇷🇺',
                  """
    `1234567890-=
    йцукенгшщзхъ
    фывапролджэ\
    /ячсмитьбю.

    ~!"№;%:?*()_+
    ЙЦУКЕНГШЩЗХЪ
    ФЫВАПРОЛДЖЭ|
    |ЯЧСМИТЬБЮ,
    """),
    'ivr': Layout('Hebrew🇮🇱',
                  """
    ~1234567890-=
    /'קראטוןםפ][
    שדגכע'חלךף,\\
    \\זסבהנמצתץ.

    ;!@#$%^&*)(_+
    QWERTYUIOP}{
    ASDFGHJKL:\"|
    |ZXCVBNM><?
    """, False)
}
back_sign = '~'


@bot.message_handler(commands=['start', 'help'])
def start(m):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(
        types.InlineKeyboardButton(
            "Eng",
            switch_inline_query="Ghbdsn!"
        ),
        types.InlineKeyboardButton(
            "Ukr",
            switch_inline_query="Руддщ!"
        ),
        types.InlineKeyboardButton(
            "Heb",
            switch_inline_query="vku!"
        )
    )
    bot.send_message(
        m.from_user.id,
        "Введіть текст, будь ласка !\n" +
        "Input text, please !\n" +
        "קלט טקסט, בבקשה!\n",
        reply_markup=buttons
    )


@bot.message_handler(content_types=['text'])
def main(m, edit=False):
    text = m.text
    _layouts = []
    output_text = ''
    for layout in layouts.values():
        if text[0] in layout:
            _layouts.append(layout)
    for layout in _layouts:
        for another_layout in layouts.values():
            output_text += another_layout.name+'\n' +\
                layout.translit(another_layout, text)+'\n\n'
    if not edit:
        return bot.send_message(m.chat.id, output_text)
    return output_text


@bot.edited_message_handler(content_types=['text'])
def edit(m):
    return bot.edit_message_text(
        main(m, True),
        m.chat.id,
        m.message_id+1
    )


@bot.inline_handler(lambda query: True)
def main_inline(query):
    text = query.query
    button = types.InlineKeyboardMarkup()
    random_ = next(random_list)
    if text:
        _layouts = []
        desc = []
        title = []
        for layout in layouts.values():
            if text[0] in layout:
                _layouts.append(layout)
        for layout in _layouts:
            for another_layout in layouts.values():
                title += [layout.translit(another_layout, text)]
                desc += [another_layout.name]
        output_text = title
    else:
        button.add(
            telebot.types.InlineKeyboardButton(
                "🔄",
                switch_inline_query_current_chat="Ghbdsn!"
            )
        )
        random_ = True
        title = ['Input some text']
        output_text = ['Reset']
        desc = [None]
    if random_:
        button.add(types.InlineKeyboardButton(
            'Підтримати проект',
            url='https://send.monobank.ua/21gs4e2aR'
        ))
    results = [telebot.types.InlineQueryResultArticle(
        f'{query.id}{i}',
        title[i],
        telebot.types.InputTextMessageContent(message_text=output_text[i]),
        button if random_ else None,
        description=desc[i]
    ) for i in range(len(title))]

    bot.answer_inline_query(query.id, results)


if __name__ == '__main__':
    bot.polling(none_stop=True)
