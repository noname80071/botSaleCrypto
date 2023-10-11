from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text='📝 Информация', callback_data='info')],
    [InlineKeyboardButton(text='💳 Купить TRON TRX', callback_data='buy_trx'),
    InlineKeyboardButton(text='💰 Профиль', callback_data='profile')]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='◀️ Выйти в меню')]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='◀️ Выйти в меню', callback_data='menu')]])

buy_menu = [
    [InlineKeyboardButton(text='Выбрать способ оплаты', callback_data='pay_method'),
     InlineKeyboardButton(text='Назад', callback_data='buy_trx')]
]

buy_menu = InlineKeyboardMarkup(inline_keyboard=buy_menu)

pay_method_menu = [
    [InlineKeyboardButton(text='CRYPTOBOT', callback_data='cryptobot'),
     InlineKeyboardButton(text='Назад', callback_data='buy_trx')]
]
pay_method_menu = InlineKeyboardMarkup(inline_keyboard=pay_method_menu)

pay_success = [
    [InlineKeyboardButton(text='Проверить оплату', callback_data='pay_success')]
]
pay_success = InlineKeyboardMarkup(inline_keyboard=pay_success)
