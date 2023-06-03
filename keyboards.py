from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.db import get_rub, get_ua

sub = InlineKeyboardButton(text='Подписаться', url='https://t.me/+qxXLHSc1P2U1ZjY9')
check_sub = InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')
sub_btn = InlineKeyboardMarkup(row_width=1).add(sub, check_sub)

back_menu = InlineKeyboardButton(text='Назад', callback_data='main_menu')
back_btn = InlineKeyboardMarkup(row_width=1).add(back_menu)
mailing = InlineKeyboardButton(text='💌 Рассылка', callback_data='mailing')
statistics = InlineKeyboardButton(text='📈 Статистика', callback_data='stat')



async def keyboard():
    get_ru = await get_rub()
    get_uah = await get_ua()
    #print(rounded_x)
    menu = InlineKeyboardMarkup()
    menu.add(InlineKeyboardButton('Как это работает', callback_data='how_work'))
    menu.row(*[InlineKeyboardButton('Обмен', callback_data='excange'),
               InlineKeyboardButton('Доставка', callback_data='delivery')])
    menu.add(InlineKeyboardButton('Выкуп', callback_data='buy'))
    menu.add(InlineKeyboardButton('Правила и условия', callback_data='rules'))
    menu.add(InlineKeyboardButton('Напишите нам', url='https://t.me/EvgeniiSergeevMSK'))
    # valuta = InlineKeyboardButton(text='Rub/Cny|Uah/Cny 🇷🇺 11.05|🇺🇦 5.41', callback_data='valuta')
    #valuta = InlineKeyboardButton(text='🇨🇳 1 ≈ 0.087₽ 🇷🇺 | 🇨🇳 1 ≈ 0.189₴ 🇺🇦', callback_data='valuta')
    menu.add(InlineKeyboardButton(f'🇨🇳 1 ≈ {get_ru}₽ 🇷🇺 | 🇨🇳 1 ≈ {get_uah}₴ 🇺🇦', callback_data='valuta'))
    return menu

how_order = InlineKeyboardButton(text='Как заказать', callback_data='how_order')
get_blank = [InlineKeyboardButton(text='Получить бланк', callback_data='get_blank'),
             InlineKeyboardButton(text='Отправить бланк', callback_data='send_blank')]

buy_btn = InlineKeyboardMarkup(row_width=1).add(how_order).row(*get_blank).add(back_menu)

instrukcia = InlineKeyboardButton(text='Инструкция', callback_data='inst')
instrukcia_btn = InlineKeyboardMarkup(row_width=1).add(instrukcia, back_menu)
instrukcia_btn_2 = InlineKeyboardMarkup(row_width=1).row(*get_blank).add(back_menu)

contact_sup = InlineKeyboardButton(text='Обменять', url='https://t.me/EvgeniiSergeevMSK')
sup_btn = InlineKeyboardMarkup(row_width=1).add(contact_sup, back_menu)

change_cur = [InlineKeyboardButton(text='♻️ Сменить курс', callback_data='change_cur')]
change_rub = [InlineKeyboardButton(text='🇷🇺|🇨🇳', callback_data='rub_cn'),
             InlineKeyboardButton(text='🇺🇦|🇨🇳', callback_data='ua_cn')]

admin = InlineKeyboardMarkup(row_width=2).row(*change_cur).add(mailing, statistics)
admin_btn = InlineKeyboardMarkup(row_width=1).row(*change_rub)

adm_menu = InlineKeyboardButton(text='Админ меню', callback_data='adm_men')
us_menu = InlineKeyboardButton(text='Юзер меню', callback_data='us_menu')
ch_menu = InlineKeyboardMarkup(row_width=2).add(adm_menu, us_menu)


back = InlineKeyboardButton(text='Назад↩', callback_data='back')
#back_btn = InlineKeyboardMarkup(row_width=1).add(back)
with_button = InlineKeyboardButton(text='С кнопкой', callback_data='button')
without_button = InlineKeyboardButton(text='Без кнопки', callback_data='without_button')
choice_btn = InlineKeyboardMarkup(row_width=2).add(with_button, without_button)