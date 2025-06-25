import json
import os

DATA_FILE = 'data/wallets.json'

def save_wallet(coin, address, private_key):
    wallet_data = {
        "coin": coin,
        "address": address,
        "private_key": private_key
    }

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(wallet_data)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
