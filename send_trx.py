from tronpy import Tron
from tronpy.keys import PrivateKey

import config


class Trons:
    def __init__(self):
        self.WALLET_ADDRESS = config.wallet_address
        self.PRIVATE_KEY = config.wallet_private_key
        self.client = Tron()

    async def send_tron(self, amount, wallet):
        amount = amount * 1000000
        priv_key = PrivateKey(bytes.fromhex(self.PRIVATE_KEY))
        # create transaction and broadcast it
        txn = (
            self.client.trx.transfer(self.WALLET_ADDRESS, wallet, amount)
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        print(f'TRON {txn.txid}')
        return txn.txid
