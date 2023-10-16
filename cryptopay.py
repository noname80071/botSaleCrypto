import config
import nest_asyncio
from aiocryptopay import AioCryptoPay, Networks

nest_asyncio.apply()


class Payment:
    def __init__(self):
        self.crypto = AioCryptoPay(token=config.CRYPTOPAY_TOKEN_TEST, network=Networks.TEST_NET)

    async def create_invoice(self, amount_usd):
        invoice = await self.crypto.create_invoice(asset='USDT', amount=amount_usd)

        return invoice.pay_url, invoice.invoice_id

    async def success_invoice(self, invoice_id):
        invoice_success = await self.crypto.get_invoices(invoice_ids=invoice_id)
        return invoice_success.status

    async def exchange(self, amount):
        exchange_amount = await self.crypto.get_amount_by_fiat(summ=amount, asset='USDT', target='RUB')

        return round(exchange_amount, 2)

