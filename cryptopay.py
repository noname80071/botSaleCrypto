import config
import nest_asyncio

nest_asyncio.apply()

from aiocryptopay import AioCryptoPay, Networks


class Payment:
    def __init__(self, amount=0, amount_usd=0):
        crypto = AioCryptoPay(token=config.CRYPTOPAY_TOKEN_TEST, network=Networks.TEST_NET)
        self.crypto = crypto
        self.amount = amount
        self.amount_usd = amount_usd

    async def create_invoice(self):
        invoice = await self.crypto.create_invoice(asset='USDT', amount=self.amount_usd)

        return invoice.pay_url, invoice.invoice_id

    async def success_invoice(self, invoice_id):
        invoice_success = await self.crypto.get_invoices(invoice_ids=invoice_id)
        return invoice_success.status

    async def exchange(self):
        exchange_amount = await self.crypto.get_amount_by_fiat(summ=self.amount, asset='USDT', target='RUB')
        return round(exchange_amount, 2)

