from aiogram.filters.state import State, StatesGroup


class SetPrice(StatesGroup):
    step_set_price = State()


class PaymentSuccess(StatesGroup):
    payment_success = State()


class PayBalance(StatesGroup):
    pay_balance = State()


class SetWallet(StatesGroup):
    set_wallet = State()


class SearchId(StatesGroup):
    search_id = State()


class AddUserBalance(StatesGroup):
    add_user_balance = State()


class DeductUserBalance(StatesGroup):
    deduct_user_balance = State()

