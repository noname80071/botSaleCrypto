from aiogram.filters.state import State, StatesGroup


class SetPrice(StatesGroup):
    step_set_price = State()


class PaymentSuccess(StatesGroup):
    payment_success = State()
