from aiogram import F, Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import requests

import kb
import text
import states
import config
import cryptopay
import connect_db
import send_trx


router = Router()
db = connect_db.BDBConnector()
cryptopay = cryptopay.Payment()
trx = send_trx.Trons()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(f'{text.greet.format(name=msg.from_user.full_name)}',
                     reply_markup=kb.menu, parse_mode='HTML')
    await db.add_user(user_id=msg.from_user.id, name=msg.from_user.full_name)


@router.callback_query(F.data == 'info')
async def info(clbck: CallbackQuery):
    await clbck.message.answer(text.info.format(suc_trans=config.suc_transactions),
                               reply_markup=kb.menu, parse_mode='HTML')


@router.callback_query(F.data == 'profile')
async def profile(clbck: CallbackQuery):
    user_balance = await db.get_balance(clbck.from_user.id)
    total_amount = await db.get_total_amount(clbck.from_user.id)
    suc_trans = await db.get_suc_transactions(clbck.from_user.id)
    await clbck.message.answer(text.profile_info.format(user_id=clbck.from_user.id,
                                                        user_balance=user_balance,
                                                        total_amount=total_amount,
                                                        suc_trans=suc_trans),
                               reply_markup=kb.menu,
                               parse_mode='HTML')


@router.callback_query(F.data == 'pay_balance')
async def pay_balance(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.pay_balance)
    await state.set_state(states.PayBalance.pay_balance)


@router.message(states.PayBalance.pay_balance)
async def pay_balance_message(msg: Message, state: FSMContext):
    await state.clear()
    amount = float(msg.text)
    await db.set_amount(user_id=msg.from_user.id, new_amount=amount)
    await msg.answer(text=text.pay_method_text,
                     reply_markup=kb.pay_balance_menu)


@router.callback_query(F.data == 'buy_trx')
async def buy_trx(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.sum_trx_buy)

    await state.set_state(states.SetPrice.step_set_price)


@router.message(states.SetPrice.step_set_price)
async def buy_trx_message(msg: Message, state: FSMContext):
    await state.clear()
    await db.set_amount(user_id=msg.from_user.id, new_amount=float(msg.text))
    await db.set_amount_trx(user_id=msg.from_user.id, new_amount_trx=round(float(msg.text) / 12, 1))
    exchange = await cryptopay.exchange(amount=float(msg.text))
    await db.set_amount_usd(user_id=msg.from_user.id, new_amount_usd=exchange)

    amount = await db.get_amount(msg.from_user.id)
    amount_changed = await db.get_amount_trx(msg.from_user.id)
    balance = await db.get_balance(msg.from_user.id)
    await msg.answer(text.buy_trx_message.format(amount=amount,
                                                 amount_change=amount_changed,
                                                 user_balance=balance),
                     reply_markup=kb.buy_menu)


@router.callback_query(F.data == 'pay_method')
async def pay_method(clbck: CallbackQuery):
    await clbck.message.answer(text.pay_method_text,
                               reply_markup=kb.pay_method_menu)


@router.callback_query(F.data == 'cryptobot')
async def crypto_pay(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(states.PaymentSuccess.payment_success)
    amount = await db.get_amount(user_id=clbck.from_user.id)
    amount_usd = await cryptopay.exchange(amount=amount)
    payment = await cryptopay.create_invoice(amount_usd=amount_usd)
    pay_url = payment[0]
    await db.set_invoice_id(user_id=clbck.from_user.id, new_invoice_id=payment[1])
    await clbck.message.answer(text=text.pay_balance_link.format(amount_usd=amount_usd, pay_url=pay_url),
                               reply_markup=kb.pay_success)


@router.callback_query(F.data == 'from_balance')
async def set_wallet(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text=text.set_wallet)
    await state.set_state(states.SetWallet.set_wallet)


@router.message(states.SetWallet.set_wallet)
async def set_wallet_number(msg: Message, state: FSMContext):
    await db.set_number_wallet(user_id=msg.from_user.id, number_wallet=msg.text)
    number_wallet = await db.get_number_wallet(user_id=msg.from_user.id)
    await msg.answer(text=text.set_wallet_success.format(user_wallet=number_wallet),
                     reply_markup=kb.wallet_success)


@router.callback_query(F.data == 'wallet_success')
async def set_wallet_success(clbck: CallbackQuery):
    balance = await db.get_balance(user_id=clbck.from_user.id)
    amount_trx = await db.get_amount_trx(user_id=clbck.from_user.id)
    amount = await db.get_amount(user_id=clbck.from_user.id)
    wallet = await db.get_number_wallet(user_id=clbck.from_user.id)
    try:
        if amount > balance:
            await clbck.message.answer(text=text.remove_balance_success)
        else:
            transaction_id = await trx.send_tron(amount=amount_trx, wallet=wallet)
            try:
                await db.sub_balance(user_id=clbck.from_user.id, amount=amount)
                await db.set_suc_transactions(user_id=clbck.from_user.id)
                await clbck.message.answer(text=text.pay_trx_success.format(amount_trx=amount_trx,
                                                                            user_wallet=f'{wallet[0:2]}...{wallet[-4:-1]}',
                                                                            transaction_id=transaction_id,
                                                                            amount=amount))
            except Exception as e:
                print(e)
                await clbck.message.answer(text=text.pay_unsuccess)
    except Exception as e:
        print(e)
        await clbck.message.answer(text=text.pay_unsuccess)


@router.callback_query(F.data == 'pay_success', states.PaymentSuccess.payment_success)
async def pay_success(clbck: CallbackQuery, state: FSMContext):
    amount = await db.get_amount(clbck.from_user.id)
    last_invoice_id = await db.get_last_invoice_id(clbck.from_user.id)
    pay_status = await cryptopay.success_invoice(last_invoice_id)
    if pay_status == 'paid':
        await clbck.message.answer(text.pay_success.format(amount=amount))
        await state.clear()
        await db.pay_balance(user_id=clbck.from_user.id, amount=amount)
        await db.set_total_balance(user_id=clbck.from_user.id, amount=amount)
    else:
        await clbck.message.answer(text=text.pay_unsuccess)
