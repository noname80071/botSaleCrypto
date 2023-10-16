from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text='📝 Информация', callback_data='info')],
    [InlineKeyboardButton(text='💳 Купить TRON TRX', callback_data='buy_trx'),
     InlineKeyboardButton(text='💰 Пополнение баланса', callback_data='pay_balance')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile')]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)

buy_menu = [
    [InlineKeyboardButton(text='Выбрать способ оплаты', callback_data='pay_method'),
     InlineKeyboardButton(text='Назад', callback_data='buy_trx')]
]

buy_menu = InlineKeyboardMarkup(inline_keyboard=buy_menu)

pay_method_menu = [
    [InlineKeyboardButton(text='Баланс профиля', callback_data='from_balance')],
    [InlineKeyboardButton(text='Назад', callback_data='buy_trx')]
]
pay_method_menu = InlineKeyboardMarkup(inline_keyboard=pay_method_menu)
pay_balance_menu = [
    [InlineKeyboardButton(text='CRYPTOBOT', callback_data='cryptobot'),
     InlineKeyboardButton(text='Отмена', callback_data='pay_balance')]
]
pay_balance_menu = InlineKeyboardMarkup(inline_keyboard=pay_balance_menu)
pay_success = [
    [InlineKeyboardButton(text='Проверить оплату', callback_data='pay_success')]
]
from_balance_success = [
    [InlineKeyboardButton(text='Подтвердить', callback_data='from_balance_success'),
     InlineKeyboardButton(text='Отмена', callback_data='pay_method')]]
from_balance_success = InlineKeyboardMarkup(inline_keyboard=from_balance_success)

pay_success = InlineKeyboardMarkup(inline_keyboard=pay_success)
