import telebot
from telebot import types
from config import token
from random import choice
random_list = (choice((0,)*(20-1)+(1,)) for i in range(100000))

bot = telebot.TeleBot(token)


class Layout:
    def __init__(self, name, value, what_different='', have_big_letters=True):
        self.name = name
        self.big = have_big_letters
        value = value.replace('\n', '').replace('    ', '')
        self.value = value[:96]
        self.spec = value[96:]
        if not self.spec:
            self.spec = self.value
        self.dif = what_different

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
    фывапролджэ\\
    /яч©ми™ь«»/

    ~!’₴€%:?*{}–±
    ЙЦЎКЁНГШЩЗХЪ
    ФЫВАПРОЛДЖЭ|
    |ЯЧСМИТЬ„“…
    """, what_different='іїє'),
    'rus': Layout('Russian🇷🇺',
                  """
    ё1234567890-=
    йцукенгшщзхъ
    фывапролджэ\\
    /ячсмитьбю.

    Ё!"№;%:?*()_+
    ЙЦУКЕНГШЩЗХЪ
    ФЫВАПРОЛДЖЭ|
    |ЯЧСМИТЬБЮ,
    """, what_different='ыъэё'),
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
    """, have_big_letters=False)
}


@bot.message_handler(commands=['start', 'help'])
def start(m):
    buttons = types.InlineKeyboardMarkup()
    buttons.row(
        types.InlineKeyboardButton(
            "Eng->Ukr",
            switch_inline_query="Ghbdsn!"
        ),
        types.InlineKeyboardButton(
            "Eng->Rus",
            switch_inline_query="Ghbdtn!"
        )
    )
    buttons.row(
        types.InlineKeyboardButton(
            "Ukr",
            switch_inline_query="Руддщ!"
        ),
        types.InlineKeyboardButton(
            "Rus",
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
        "Enter text, please !\n" +
        "קלט טקסט, בבקשה!\n",
        reply_markup=buttons
    )


def translit(text):
    _layouts = []
    __layouts = []
    output_text = []
    output_title = []
    for layout in layouts.values():
        if text[0] in layout:
            __layouts.append(layout)
    if len(_layouts) > 1:
        for layout in __layouts:
            if any([(i in text) for i in layout.dif]):
                _layouts.append(layout)
    for layout in _layouts:
        for another_layout in layouts.values():
            output_text += [layout.translit(another_layout, text)]
            output_title += [layout.name+'->'+another_layout.name]
    return output_text, output_title


@bot.message_handler(content_types=['text'])
def main(m):
    text = m.text
    out = translit(text)
    output = ''.join([o1+'\n'+o2+'\n\n' for o1,o2 in out])
    return bot.send_message(m.chat.id, output)


@bot.edited_message_handler(content_types=['text'])
def edit(m):
    text = m.text
    out = translit(text)
    output = ''.join([o1+'\n'+o2+'\n\n' for o1,o2 in out])
    try:
        return bot.edit_message_text(
            output,
            m.chat.id,
            m.message_id+1
        )
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: True)
def main_inline(query):
    text = query.query
    button = types.InlineKeyboardMarkup()
    random_ = next(random_list)
    if text:
        desc, title = translit(text)
        output_text = title
    else:
        button.add(
            telebot.types.InlineKeyboardButton(
                "🔄",
                switch_inline_query_current_chat="Ghbdtn!"
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
