from aiogram import F, Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import requests

import kb
import text
import states
import user_data
import config
import cryptopay


router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(f'{text.greet.format(name=msg.from_user.full_name)}',
                     reply_markup=kb.menu, parse_mode='HTML')


@router.callback_query(F.data == 'info')
async def info(clbck: CallbackQuery):
    await clbck.message.answer(text.info.format(suc_trans=config.suc_transactions),
                               reply_markup=kb.menu, parse_mode='HTML')


@router.callback_query(F.data == 'profile')
async def profile(clbck: CallbackQuery):
    await clbck.message.answer(text.profile_info.format(user_id=clbck.from_user.id,
                                                        user_balance=user_data.user_balance,
                                                        total_amount=user_data.user_total_amount,
                                                        suc_trans=user_data.suc_transactions),
                               reply_markup=kb.menu,
                               parse_mode='HTML')


@router.callback_query(F.data == 'buy_trx')
async def buy_trx(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.sum_trx_buy)

    await state.set_state(states.SetPrice.step_set_price)


@router.message(states.SetPrice.step_set_price)
async def buy_trx_message(msg: Message, state: FSMContext):
    await state.clear()
    user_data.amount = float(msg.text)
    user_data.amount_change = round(user_data.amount / 12, 1)
    exchange = cryptopay.Payment(amount=user_data.amount)
    user_data.amount_usd = await exchange.exchange()
    await msg.answer(text.buy_trx_message.format(amount=user_data.amount,
                                                 amount_change=user_data.amount_change),
                     reply_markup=kb.buy_menu)
    return user_data.amount, user_data.amount_change, user_data.amount_usd


@router.callback_query(F.data == 'pay_method')
async def pay_method(clbck: CallbackQuery):
    await clbck.message.answer(text.pay_method_text,
                               reply_markup=kb.pay_method_menu)


@router.callback_query(F.data == 'cryptobot')
async def crypto_pay(clbck: CallbackQuery, state: FSMContext): # Переделать когда сделаю базу.
    await state.set_state(states.PaymentSuccess.payment_success)
    payment = cryptopay.Payment(amount_usd=user_data.amount_usd)
    payment = await payment.create_invoice()
    pay_url = payment[0]
    user_data.user_invoice_id = payment[1]

    await clbck.message.answer(text=f'Чтобы оплатить {user_data.amount_usd} USD, перейдите по ссылке: {pay_url}',
                               reply_markup=kb.pay_success)


@router.callback_query(F.data == 'pay_success', states.PaymentSuccess.payment_success)
async def pay_success(clbck: CallbackQuery, state: FSMContext):
    pay_suc = cryptopay.Payment()
    pay_status = await pay_suc.success_invoice(user_data.user_invoice_id)
    if pay_status == 'paid':
        await clbck.message.answer(text.pay_success.format(amount=user_data.amount))
        await state.clear()
    else:
        await clbck.message.answer(text=text.pay_unsuccess)
