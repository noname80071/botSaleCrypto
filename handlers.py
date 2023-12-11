from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


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
    if msg.from_user.id in config.ADMIN_ID:
        await msg.answer(text='Вы авторизировались как администратор!')
        await msg.answer(text=f'{text.greet.format(name=msg.from_user.full_name)}',
                         reply_markup=kb.menu_for_admin)
    else:
        await msg.answer(text=f'{text.greet.format(name=msg.from_user.full_name)}',
                         reply_markup=kb.menu)
        await db.add_user(user_id=msg.from_user.id, name=msg.from_user.full_name)


@router.callback_query(F.data == 'menu')
async def menu(clbck: CallbackQuery):
    if clbck.from_user.id in config.ADMIN_ID:
        await clbck.message.edit_text(text=f'{text.greet.format(name=clbck.message.from_user.full_name)}',
                                   reply_markup=kb.menu_for_admin)
    else:
        await clbck.message.edit_text(text=f'{text.greet.format(name=clbck.message.from_user.full_name)}',
                                   reply_markup=kb.menu)


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(clbck: CallbackQuery):
    await clbck.message.edit_text(text='Добро пожаловать в админ панель!',
                                  reply_markup=kb.admin_panel)


@router.callback_query(F.data == 'user_info_panel')
@router.callback_query(F.data == 'search_id')
async def search_id(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text='Введите ID пользователя.')
    await state.set_state(states.SearchId.search_id)


@router.message(states.SearchId.search_id)
async def search_id_enter(msg: Message, state: FSMContext):
    try:
        await state.clear()
        config.search_id = int(msg.text)
        user_info = await db.search_user_info(config.search_id)
        await msg.answer(text=text.user_info.format(username=user_info[0],
                                                    user_id=config.search_id,
                                                    user_balance=user_info[1],
                                                    user_total_amount=user_info[2],
                                                    user_suc_transactions=user_info[3]),
                         reply_markup=kb.user_info_panel)
    except Exception as e:
        await msg.answer(text='Такого пользователя несуществует',
                         reply_markup=kb.user_info_back)
        print(e)


@router.callback_query(F.data == 'add_user_balance')
async def set_add_user_balance(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text='Введите сумму пополнения кошелька пользователя',
                                  reply_markup=kb.user_info_back)
    await state.set_state(states.AddUserBalance.add_user_balance)


@router.callback_query(F.data == 'deduct_user_balance')
async def set_deduct_user_balance(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text='Введите сумму вычитания кошелька пользователя',
                                  reply_markup=kb.user_info_back)
    await state.set_state(states.DeductUserBalance.deduct_user_balance)


@router.message(states.DeductUserBalance.deduct_user_balance)
async def deduct_user_balance(msg: Message, state: FSMContext):
    await state.clear()
    amount_balance = float(msg.text)
    await db.sub_balance(user_id=config.search_id, amount=amount_balance)
    await msg.answer(text='Баланс пользователя успешно изменён.',
                     reply_markup=kb.user_info_back)


@router.message(states.AddUserBalance.add_user_balance)
async def add_user_balance(msg: Message, state: FSMContext):
    await state.clear()
    amount_balance = float(msg.text)
    await db.pay_balance(user_id=config.search_id, amount=amount_balance)
    await msg.answer(text='Баланс пользователя успешно изменён',
                     reply_markup=kb.user_info_back)


@router.callback_query(F.data == 'info')
async def info(clbck: CallbackQuery):
    await clbck.message.edit_text(text.info.format(suc_trans=config.suc_transactions),
                                  reply_markup=kb.menu, parse_mode='HTML')


@router.callback_query(F.data == 'profile')
async def profile(clbck: CallbackQuery):
    user_balance = await db.get_balance(clbck.from_user.id)
    total_amount = await db.get_total_amount(clbck.from_user.id)
    suc_trans = await db.get_suc_transactions(clbck.from_user.id)
    await clbck.message.edit_text(text.profile_info.format(user_id=clbck.from_user.id,
                                                           user_balance=user_balance,
                                                           total_amount=total_amount,
                                                           suc_trans=suc_trans),
                                  reply_markup=kb.menu,
                                  parse_mode='HTML')


@router.callback_query(F.data == 'pay_balance')
async def pay_balance(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.pay_balance,
                                  reply_markup=kb.back_menu)
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
    await clbck.message.edit_text(text.sum_trx_buy,
                                  reply_markup=kb.back_menu)

    await state.set_state(states.SetPrice.step_set_price)


@router.message(states.SetPrice.step_set_price)
async def buy_trx_message(msg: Message, state: FSMContext):
    await state.clear()
    await db.set_amount(user_id=msg.from_user.id, new_amount=round(float(msg.text), 1) * 12)
    await db.set_amount_trx(user_id=msg.from_user.id, new_amount_trx=round(float(msg.text), 1))
    exchange = await cryptopay.exchange(amount=round(float(msg.text), 1) * 12)
    await db.set_amount_usd(user_id=msg.from_user.id, new_amount_usd=exchange)

    amount = await db.get_amount(msg.from_user.id)
    amount_trx = await db.get_amount_trx(msg.from_user.id)
    amount_changed = await db.get_amount_trx(msg.from_user.id)
    balance = await db.get_balance(msg.from_user.id)
    if amount_trx < 5:
        await msg.answer(text=text.small_amount_trx.format(amount_trx=amount_trx),
                         reply_markup=kb.fail_set_amount)
        return
    await msg.answer(text.buy_trx_message.format(amount=amount,
                                                 amount_change=amount_changed,
                                                 user_balance=balance),
                     reply_markup=kb.buy_menu)


@router.callback_query(F.data == 'pay_method')
async def pay_method(clbck: CallbackQuery):
    await clbck.message.edit_text(text.pay_method_text,
                                  reply_markup=kb.pay_method_menu)


@router.callback_query(F.data == 'cryptobot')
async def crypto_pay(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(states.PaymentSuccess.payment_success)
    amount = await db.get_amount(user_id=clbck.from_user.id)
    amount_usd = await cryptopay.exchange(amount=amount)
    payment = await cryptopay.create_invoice(amount_usd=amount_usd)
    pay_url = payment[0]
    await db.set_invoice_id(user_id=clbck.from_user.id, new_invoice_id=payment[1])
    await clbck.message.edit_text(text=text.pay_balance_link.format(amount_usd=amount_usd, pay_url=pay_url),
                                  reply_markup=kb.pay_success)


@router.callback_query(F.data == 'from_balance')
async def set_wallet(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text=text.set_wallet,
                                  reply_markup=kb.back_menu)
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
            await clbck.message.edit_text(text=text.remove_balance_unsuccess)
        else:
            transaction_id = await trx.send_tron(amount=amount_trx, wallet=wallet)
            try:
                await db.sub_balance(user_id=clbck.from_user.id, amount=amount)
                await db.set_suc_transactions(user_id=clbck.from_user.id)
                await clbck.message.edit_text(text=text.pay_trx_success.format(amount_trx=amount_trx,
                                                                               user_wallet=f'{wallet[0:2]}...{wallet[-4:-1]}',
                                                                               transaction_id=transaction_id,
                                                                               amount=amount))
            except Exception as e:
                print(e)
                await clbck.message.edit_text(text=text.pay_unsuccess)
    except Exception as e:
        print(e)
        await clbck.message.edit_text(text=text.pay_unsuccess)


@router.callback_query(F.data == 'pay_success', states.PaymentSuccess.payment_success)
async def pay_success(clbck: CallbackQuery, state: FSMContext):
    amount = await db.get_amount(clbck.from_user.id)
    last_invoice_id = await db.get_last_invoice_id(clbck.from_user.id)
    pay_status = await cryptopay.success_invoice(last_invoice_id)
    if pay_status == 'paid':
        await clbck.message.edit_text(text.pay_success.format(amount=amount),
                                      reply_markup=kb.back_menu)
        await state.clear()
        await db.pay_balance(user_id=clbck.from_user.id, amount=amount)
        await db.set_total_balance(user_id=clbck.from_user.id, amount=amount)
    else:
        await clbck.message.answer(text=text.pay_unsuccess,
                                   reply_markup=kb.back_menu)
