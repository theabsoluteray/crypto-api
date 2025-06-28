from web3 import Web3
import os
from dotenv import load_dotenv
from config import GAS_LIMIT_ETH, OVERRIDE_GAS_PRICE_GWEI
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
    try:
        acct = w3.eth.account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(acct.address)

        gas_limit = GAS_LIMIT_ETH
        gas_price = w3.toWei(OVERRIDE_GAS_PRICE_GWEI, 'gwei') if OVERRIDE_GAS_PRICE_GWEI else w3.eth.gas_price
        gas_fee_eth = w3.fromWei(gas_limit * gas_price, 'ether')

        if amount <= gas_fee_eth:
            raise ValueError("Amount too low to cover gas fees")

        value_eth = amount - gas_fee_eth
        value_wei = w3.toWei(value_eth, 'ether')

        tx = {
            'to': to_address,
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
        }

        signed_tx = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    except ValueError as ve:
        return f"ValueError: {str(ve)}"
    except Exception as e:
        return f"Error: {str(e)}"