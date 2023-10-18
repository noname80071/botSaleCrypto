from tronpy import Tron, Contract
from tronpy.keys import PrivateKey

client = Tron()
wallet = client.generate_address()
print("Wallet address:  %s" % wallet['base58check_address'])
print("Private Key:  %s" % wallet['private_key'])

Account_addr = wallet['base58check_address']