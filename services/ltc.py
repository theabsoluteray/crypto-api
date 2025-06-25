from block_io import BlockIo
import os
from dotenv import load_dotenv

load_dotenv()

BLOCK_IO_API_KEY = os.getenv('BLOCK_IO_API_KEY')
BLOCK_IO_PIN = os.getenv('BLOCK_IO_PIN') or None
block_io = BlockIo(BLOCK_IO_API_KEY, BLOCK_IO_PIN, 2)

def create_wallet():
    res = block_io.get_new_address()
    return {
        'address': res['data']['address'],
        'private_key': 'managed_by_blockio'
    }

def get_balance(address):
    res = block_io.get_address_balance(addresses=address)
    return float(res['data']['available_balance'])

def send_ltc(_private_key, to_address, amount):
    res = block_io.withdraw(
        amounts=str(amount),
        to_addresses=to_address,
        priority='low'
    )
    return res['data']['txid']
