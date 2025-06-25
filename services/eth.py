from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv('INFURA_URL')
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def create_wallet():
    acct = w3.eth.account.create()
    return {
        "address": acct.address,
        "private_key": acct.key.hex()
    }

def get_balance(address):
    balance_wei = w3.eth.get_balance(address)
    return float(w3.fromWei(balance_wei, 'ether'))

def send_eth(private_key, to_address, amount):
    acct = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(acct.address)
    tx = {
        'to': to_address,
        'value': w3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    signed_tx = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()
