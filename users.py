from data.db import create_profile
from loader import dp, bot, types
from settings.config import channel_id
from settings.func import check_sub_channel
from settings.keyboards import *
from settings.text import *


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=open('china.jpg', 'rb'),
            caption=f'{start_msg}',
            parse_mode='html',
            reply_markup=await keyboard()
        )
        await create_profile(user_id=message.from_user.id)
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Для использования бота, вам нужно подписаться на канал',
            reply_markup=sub_btn
        )

@dp.callback_query_handler(text='check_sub')
async def subb(call: types.CallbackQuery):
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await call.answer(
            text='Вы подписаны',
            show_alert=True
        )
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=open('china.jpg', 'rb'),
            caption=f'{start_msg}',
            parse_mode='html',
            reply_markup=await keyboard()
        )
        await create_profile(user_id=call.from_user.id)
    else:
        await call.answer(
            text='Для пользования ботом, нужно подписаться на канал !',
            show_alert=True
        )

@dp.callback_query_handler(text=['how_work','excange','delivery','buy', 'main_menu', 'rules', 'inst'])
async def all_call(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == 'how_work':
        await bot.edit_message_caption(
            chat_id=user_id,
            message_id=call.message.message_id,
            caption=f'{how_work_text}',
            parse_mode='html',
            reply_markup=back_btn
        )
    elif call.data == 'excange':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{exchange_text}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=sup_btn
        )
    elif call.data == 'delivery':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{how_work_text}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=instrukcia_btn
        )
    elif call.data == 'buy':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{buy_text}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=buy_btn
        )
    elif call.data == 'valuta':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption='Rub/Cny',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=back_btn
        )
    elif call.data == 'main_menu':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{start_msg}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=await keyboard()
        )
    elif call.data == 'rules':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{rules_text}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=back_btn
        )
    elif call.data == 'inst':
        await bot.edit_message_caption(
            chat_id=user_id,
            caption=f'{inst_text}',
            message_id=call.message.message_id,
            parse_mode='html',
            reply_markup=instrukcia_btn
        )



