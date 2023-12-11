from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text='📝 Информация', callback_data='info')],
    [InlineKeyboardButton(text='💳 Купить TRON TRX', callback_data='buy_trx'),
     InlineKeyboardButton(text='💰 Пополнение баланса', callback_data='pay_balance')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile')]
]
menu_for_admin = [
    [InlineKeyboardButton(text='📝 Информация', callback_data='info')],
    [InlineKeyboardButton(text='💳 Купить TRON TRX', callback_data='buy_trx'),
     InlineKeyboardButton(text='💰 Пополнение баланса', callback_data='pay_balance')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile')],
    [InlineKeyboardButton(text='Админ панель', callback_data='admin_panel')]
]
menu_for_admin = InlineKeyboardMarkup(inline_keyboard=menu_for_admin)
menu = InlineKeyboardMarkup(inline_keyboard=menu)

admin_panel = [
    [InlineKeyboardButton(text='Поиск пользователя по ID', callback_data='search_id'),
     InlineKeyboardButton(text='Назад', callback_data='menu')]]

admin_panel = InlineKeyboardMarkup(inline_keyboard=admin_panel)

user_info_panel = [
    [InlineKeyboardButton(text='Прибавить баланс пользователю', callback_data='add_user_balance'),
     InlineKeyboardButton(text='Убавить баланс пользователю', callback_data='deduct_user_balance')],
    [InlineKeyboardButton(text='Назад в меню', callback_data='menu')]
]
user_info_panel = InlineKeyboardMarkup(inline_keyboard=user_info_panel)

user_info_back = [
    [InlineKeyboardButton(text='Назад', callback_data='user_info_panel')]
]
user_info_back = InlineKeyboardMarkup(inline_keyboard=user_info_back )

back_menu = [
    [InlineKeyboardButton(text='В меню', callback_data='menu')]
]
back_menu = InlineKeyboardMarkup(inline_keyboard=back_menu)

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
# from_balance_success = [
#     [InlineKeyboardButton(text='Подтвердить', callback_data='from_balance_success'),
#      InlineKeyboardButton(text='Отмена', callback_data='pay_method')]]
# from_balance_success = InlineKeyboardMarkup(inline_keyboard=from_balance_success)

pay_success = InlineKeyboardMarkup(inline_keyboard=pay_success)

wallet_success = [
    [InlineKeyboardButton(text='Подтвердить', callback_data='wallet_success'),
     InlineKeyboardButton(text='Отмена', callback_data='from_balance')]
]
wallet_success = InlineKeyboardMarkup(inline_keyboard=wallet_success)

fail_set_amount = [
    [InlineKeyboardButton(text='Назад', callback_data='buy_trx')]
]
fail_set_amount = InlineKeyboardMarkup(inline_keyboard=fail_set_amount)
