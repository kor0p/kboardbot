from functools import cache
from random import choice

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from .bot import bot


SUPER_ADMIN_ID = 320063227

random_list_gen = (choice((0,) * 19 + (1,)) for i in range(100000))
start_helper_dict = {
    'Ukr': 'Руддщ!',
    'Rus': 'Руддщ!',
    'Heb': 'vku!',
    'Eng->Ukr': 'Ghbdsn!',
    'Eng->Rus': 'Ghbdtn!'
}

languages = {
    'en': {
        'in': 'Input some text!',
        'out': 'Руддщ',
        'reset': 'Reset',
        'donate': 'Donate me:)',
        'error': 'Internal error occurred :(',
    },
    'uk': {
        'in': 'Введіть текст!',
        'out': 'Ghbdsn',
        'reset': 'Ввід',
        'donate': 'Підтримати проект:)',
        'error': 'Технічна помилка :(',
    },
    'ru': {
        'in': 'Введите текст!',
        'out': 'Ghbdtn',
        'reset': 'Ввод',
        'donate': 'Поддержать проект:)',
        'error': 'Техническая ошибка :(',
    }
}


def lang(user):
    l_code = user.language_code
    l_code = l_code or 'en'
    if '-' in l_code:
        l_code = l_code.strip('-')[0]
    return languages[l_code]


class Layout:
    def __init__(self, name, value, what_different='', have_big_letters=True):
        self.name = name
        self.big = have_big_letters
        value = value.replace('\n', '').replace(' ', '')
        self.value = value[:96]
        self.spec = value[96:]
        if not self.spec:
            self.spec = self.value
        self.dif = what_different or self.value[:48 * (self.big + 1)]

    def __repr__(self):
        return self.value + self.spec

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


ALL_LAYOUTS = {
    'eng': Layout(
        'English🇬🇧',
        '''
`1234567890-= qwertyuiop[] asdfghjkl;'\\ \\zxcvbnm,./
~!@#$%^&*()_+ QWERTYUIOP{} ASDFGHJKL:\"| |ZXCVBNM<>?
'''
    ),
    'ukr': Layout(
        'Ukrainian🇺🇦',
        '''
`1234567890-= йцукенгшщзхї фівапролджєґ /ячсмитьбю.
~!"№;%:?*()_+ ЙЦУКЕНГШЩЗХЇ ФІВАПРОЛДЖЄҐ |ЯЧСМИТЬБЮ,
́¹²§$°<>•[]—≠ йцў®ёнгшщзхъ фывапролджэ\\ /яч©ми™ь«»/
~!’₴€%:?*{}–± ЙЦЎКЁНГШЩЗХЪ ФЫВАПРОЛДЖЭ| |ЯЧСМИТЬ„“…
''',
        what_different='іїє',
    ),
    'rus': Layout(
        'Russian🇷🇺',
        '''
ё1234567890-= йцукенгшщзхъ фывапролджэ\\ /ячсмитьбю.
Ё!"№;%:?*()_+ ЙЦУКЕНГШЩЗХЪ ФЫВАПРОЛДЖЭ| |ЯЧСМИТЬБЮ,
''',
        what_different='ыъэё',
    ),
    'ivr': Layout(
        'Hebrew🇮🇱',
        '''
~1234567890-= /'קראטוןםפ][ שדגכע'חלךף,\\ \\זסבהנמצתץ.
;!@#$%^&*)(_+ QWERTYUIOP}{ ASDFGHJKL:\"| |ZXCVBNM><?
''',
        have_big_letters=False,
    ),
}


@bot.message_handler(commands=['start', 'help'])
def start(m):
    buttons = InlineKeyboardMarkup()
    buttons.add(*[
        InlineKeyboardButton(text=text, switch_inline_query=query)
        for text, query in start_helper_dict.items()
    ])
    bot.send_message(
        m.from_user.id,
        '\n'.join([_lang['in'] for _lang in languages.values()]),
        reply_markup=buttons
    )


@cache
def translit(text):
    temp_layouts = []
    layouts = []
    output_text = []
    output_title = []

    for layout in ALL_LAYOUTS.values():
        if text[0] in layout:
            layouts.append(layout)

    for layout in layouts:
        if any((i in text) for i in layout.dif):
            temp_layouts.append(layout)

    temp_layouts = temp_layouts or layouts
    for layout in temp_layouts:
        for another_layout in ALL_LAYOUTS.values():
            if layout.name == another_layout.name:
                continue

            output_text += [layout.translit(another_layout, text)]
            output_title += [layout.name + '->' + another_layout.name]
    return output_text, output_title


@bot.message_handler(content_types=['text'])
def main(m):
    output = ''.join([
        text + '\n' + title + '\n\n'
        for text, title in zip(*translit(m.text))
    ])
    return bot.send_message(m.chat.id, output)


@bot.edited_message_handler(content_types=['text'])
def edit(m):
    output = ''.join([
        text + '\n' + title + '\n\n'
        for text, title in translit(m.text)
    ])
    try:
        return bot.edit_message_text(
            output,
            m.chat.id,
            m.message_id + 1
        )
    except Exception as e:
        bot.send_message(m.chat.id, lang(m.from_user)['error'])
        bot.send_message(SUPER_ADMIN_ID, str(e))


@bot.inline_handler(lambda query: True)
def main_inline(query):
    text = query.query
    user_lang = lang(query.from_user)
    button = InlineKeyboardMarkup()

    if text:
        titles, descriptions = translit(text)
        output_text = titles
        show_donate_btn = next(random_list_gen)
    else:
        button.add(
            InlineKeyboardButton(
                text='🔄',
                switch_inline_query_current_chat=user_lang['out'],
            )
        )
        show_donate_btn = True
        titles = [user_lang['in']]
        output_text = [user_lang['reset']]
        descriptions = [None]

    if show_donate_btn:
        button.add(InlineKeyboardButton(
            text=user_lang['donate'],
            url='https://send.monobank.ua/21gs4e2aR',
        ))

    results = [
        InlineQueryResultArticle(
            id=f'{query.id}{i}',
            title=title,
            input_message_content=InputTextMessageContent(message_text=output_text[i]),
            reply_markup=button if show_donate_btn else None,
            description=description,
        )
        for i, (title, description) in enumerate(zip(titles, descriptions))
    ]

    bot.answer_inline_query(query.id, results)
