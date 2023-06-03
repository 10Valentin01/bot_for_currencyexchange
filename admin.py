from data.db import *
from loader import dp, bot, types
from settings.keyboards import *
from aiogram.dispatcher import FSMContext
from settings.state import *
from settings.text import start_msg


@dp.message_handler(commands=['admin'], state="*")
async def adm(message: types.Message, state:FSMContext):
    await state.finish()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Вы в адмни панели, выберите пункт\n'
             'Для возврата в основное меню нажмите /start',
        reply_markup=admin,

    )

@dp.callback_query_handler(text=['change_cur', 'rub_cn','ua_cn'], state="*")
async def cal_adm(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if call.data == 'change_cur':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Выберите пару, для смены курса',
            reply_markup=admin_btn
        )
    elif call.data == 'rub_cn':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Введите сколько руб 1 юань Юань\n\nПример 12.1'
        )
        await rub.ru.set()
    elif call.data == 'ua_cn':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Введите сколько гривен 1 юань Юань\n\nПример 12.1'
        )
        await uah.ua.set()


@dp.message_handler(state=rub.ru)
async def dshjf2(message: types.Message, state: FSMContext):
    x = message.text
    await change_rubb(text=x)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"<b>Курсы валют в боте</b> \n\n"
             f"<b>🇷🇺 RUB/CNY 🇨🇳 </b> =  <code>{await get_rub()}</code>\n\n"
             f"<b>🇺🇦 UAH/CNY 🇨🇳 </b> =  <code>{await get_ua()}</code>",
        # parse_mode='html',
        reply_markup=ch_menu
    )
    await state.finish()

@dp.message_handler(state=uah.ua)
async def dshjf(message: types.Message, state: FSMContext):
    x = message.text
    await change_uah(text=x)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"<b>Курсы валют в боте</b> \n\n"
             f"<b>🇷🇺 RUB/CNY 🇨🇳 </b> =  <code>{await get_rub()}</code>\n\n"
             f"<b>🇺🇦 UAH/CNY 🇨🇳 </b> =  <code>{await get_ua()}</code>",
        # parse_mode='html',
        reply_markup=ch_menu
    )
    await state.finish()

@dp.callback_query_handler(text=['adm_men', 'us_menu'])
async def adm_choice(call: types.CallbackQuery):
    if call.data == 'adm_men':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Вы в адмни панели, выберите пункт\n'
                 'Для возврата в основное меню нажмите /start',
            reply_markup=admin,
        )
    elif call.data == 'us_menu':
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=open('china.jpg', 'rb'),
            caption=f'{start_msg}',
            reply_markup=await keyboard()
        )
    else:
        print('None')


@dp.callback_query_handler(text='mailing', state="*")
async def mailing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(call.from_user.id, "Выберите действие", reply_markup=choice_btn)

@dp.callback_query_handler(text='button', state="*")
async def with_button_(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['btn'] = call.data
        if data['btn'] == 'without_button':
            await bot.send_message(call.from_user.id, "Введите текст рассылки и прикрепите фото в чат ⤵",
                                   reply_markup=back_btn, parse_mode='HTMl')
            await adminka.adminka_2.set()
        else:
            await bot.send_message(call.from_user.id, "Отправьте текст кнопки")
            await adminka.url.set()

@dp.callback_query_handler(text='without_button', state="*")
async def with_button_(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, "Введите текст рассылки и прикрепите фото в чат ⤵",
                                   reply_markup=back_btn, parse_mode='HTMl')
    await adminka.adminka_2.set()

@dp.message_handler(state=adminka.url)
async def urrl(message: types.Message, state: FSMContext):
    await state.update_data(text_btn=message.text, parse_mode='HTML')
    await bot.send_message(message.from_user.id, "Отправьте ссылку на кнопку")
    await adminka.text_message.set()

@dp.message_handler(state=adminka.text_message)
async def text_msg(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await bot.send_message(message.from_user.id, "Введите текст рассылки и прикрепите фото в чат ⤵", reply_markup=back_btn, parse_mode='HTMl')

    await adminka.mail.set()

@dp.message_handler(state=adminka.mail, content_types=('photo', 'text','video', 'animation', types.ParseMode.HTML))
async def mail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.photo) > 0:
            document_id = message.photo[0].file_id
            file_info = await bot.get_file(document_id)
            data['mail'] = message.caption
            await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
        else:
            if message["video"]:
                video_id = message.video.file_id
                file_video = await bot.get_file(video_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
            elif message["animation"]:
                file_id = message.animation.file_id
                file_animation = await bot.get_file(file_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
            else:
                data['mail'] = message.text
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")

    r = cur.execute(
        'SELECT user_id FROM users').fetchall()

    for i in r:
        try:
            if len(message.photo) > 0:
                x = InlineKeyboardButton(text=f'{data["text_btn"]}', url=f'{data["url"]}')
                x_btn = InlineKeyboardMarkup(row_width=1).add(x)
                await bot.send_photo(chat_id=i[0], photo=file_info.file_id, caption=data[
                    'mail'], parse_mode='html', reply_markup=x_btn)
            else:
                if message["video"]:
                    x = InlineKeyboardButton(text=f'{data["text_btn"]}', url=f'{data["url"]}')
                    x_btn = InlineKeyboardMarkup(row_width=1).add(x)
                    await bot.send_video(chat_id=i[0], video=file_video.file_id, caption=data[
                        'mail'], parse_mode='html', reply_markup=x_btn
                                         )
                elif message["animation"]:
                    x = InlineKeyboardButton(text=f'{data["text_btn"]}', url=f'{data["url"]}')
                    x_btn = InlineKeyboardMarkup(row_width=1).add(x)
                    await bot.send_animation(chat_id=i[0], animation=file_animation.file_id, caption=data[
                        'mail'], reply_markup=x_btn, parse_mode='html')
                else:
                    x = InlineKeyboardButton(text=f'{data["text_btn"]}', url=f'{data["url"]}')
                    x_btn = InlineKeyboardMarkup(row_width=1).add(x)
                    await bot.send_message(chat_id=i[0], text=data['mail'], parse_mode="html", reply_markup=x_btn)
                    #await bot.send_message(chat_id=5664258429, text=data['mail'], parse_mode="html", reply_markup=x_btn)

        except Exception as err:
            print(err)
        continue
    await message.answer('✅ Рассылка всем пользователям завершена', )
    await state.finish()


@dp.message_handler(state=adminka.adminka_2, content_types=types.ContentTypes.ANY)
async def mail_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.photo) > 0:
            document_id = message.photo[0].file_id
            file_info = await bot.get_file(document_id)
            data['mail'] = message.caption
            await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
        else:
            if message["video"]:
                video_id = message.video.file_id
                file_video = await bot.get_file(video_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
            elif message["animation"]:
                file_id = message.animation.file_id
                file_animation = await bot.get_file(file_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
            else:
                data['mail'] = message.text
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")

    r = cur.execute(
        'SELECT user_id FROM users').fetchall()

    for i in r:
        try:
            if len(message.photo) > 0:
                await bot.send_photo(chat_id=i[0], photo=file_info.file_id, caption=data[
                    'mail'], parse_mode='html')
            else:
                if message["video"]:
                    await bot.send_video(chat_id=i[0], video=file_video.file_id, caption=data[
                        'mail'], parse_mode='html'
                    )
                elif message["animation"]:
                   #await bot.send_message(message.from_user.id, 'Рассылка пошла')
                    await bot.send_animation(chat_id=i[0],animation=file_animation.file_id, caption=data[
                        'mail'], parse_mode='html')
                else:
                    await bot.send_message(chat_id=i[0], text=data["mail"], parse_mode='html', disable_web_page_preview=True)
        except Exception as err:
            print(err)
        continue
    await message.answer('✅ Рассылка всем пользователям завершена', )
    await state.finish()


@dp.message_handler(state=adminka.adminka_2, content_types=types.ContentTypes.ANY)
async def mail_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if len(message.photo) > 0:
            document_id = message.photo[0].file_id
            file_info = await bot.get_file(document_id)
            data['mail'] = message.caption
            await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
        else:
            if message["video"]:
                video_id = message.video.file_id
                file_video = await bot.get_file(video_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")

            elif message["animation"]:
                file_id = message.animation.file_id
                file_animation = await bot.get_file(file_id)
                data['mail'] = message.caption
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")
            else:
                data['mail'] = message.text
                await bot.send_message(chat_id=message.from_user.id, text="Рассылка пошла")

    r = cur.execute(
        'SELECT user_id FROM users').fetchall()

    for i in r:
        try:
            if len(message.photo) > 0:
                await bot.send_photo(chat_id=i[0], photo=file_info.file_id, caption=data[
                    'mail'], parse_mode='html')
            else:
                if message["video"]:
                    await bot.send_video(chat_id=i[0], video=file_video.file_id, caption=data[
                        'mail'], parse_mode='html'
                    )
                elif message["animation"]:
                    await bot.send_animation(chat_id=i[0],animation=file_animation.file_id, caption=data[
                        'mail'])
                else:
                    await bot.send_message(chat_id=i[0], text=data['mail'], parse_mode='html')
        except Exception as err:
            print(err)
        continue
    await message.answer('✅ Рассылка всем пользователям завершена', )
    await state.finish()

@dp.callback_query_handler(text='stat', state="*")
async def stat(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    sql = cur.execute("SELECT COUNT(`user_id`) FROM users")
    result = cur.fetchall()
    print(sql)
    await bot.send_message(call.from_user.id, f"👤 Всего пользователей в боте: "
                                              f"{result[0][0]}")
    await state.finish()


@dp.callback_query_handler(text='stat', state="*")
async def stat(call: types.CallbackQuery):
    sql = cur.execute("SELECT COUNT(`user_id`) FROM users")
    result = cur.fetchall()
    await bot.send_message(call.from_user.id, f"👤 Всего пользователей в боте: "
                                              f"{result[0][0]}")


@dp.callback_query_handler(text='back', state='*')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Выберите действие", reply_markup=admin)
