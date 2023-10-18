from tronpy import Tron
from tronpy.keys import PrivateKey

# your wallet information
WALLET_ADDRESS = 'TU4jdo7F64ei9Lvbfb3K71HGczsFHM3Pmd'
PRIVATE_KEY = '06f78bf338698a041b76b356a4947302da05aafb66db445814b84797689131bb'

# connect to the Testnet Tron blockchain
client = Tron()


# sending some 'amount' of nile test Tron to another nile test address

def send_tron(amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(WALLET_ADDRESS, amount, wallet)
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        print(txn.txid)

    # return the exception
    except Exception as ex:
        print("exception")
        print(ex)
        return ex


recipient_address = 'TZHfJB6G8QAZk24U1ewbrUYgQDrSAAd8nA'
amount = 1000000
send_tron(recipient_address, amount)
