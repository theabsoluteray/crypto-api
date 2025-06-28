import json
import os

DATA_FILE = 'data/wallets.json'

def save_wallet(coin, address, private_key):
    wallet_entry = {
        "address": address,
        "private_key": private_key
    }

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

 
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}

   
    if coin not in data:
        data[coin] = []

 
    data[coin].append(wallet_entry)

   
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def log_transaction(coin, txid):
    explorer_urls = {
        "btc": f"https://live.blockcypher.com/btc/tx/{txid}",
        "eth": f"https://etherscan.io/tx/{txid}",
        "ltc": f"https://live.blockcypher.com/ltc/tx/{txid}"
    }

    url = explorer_urls.get(coin, "") + txid
    os.makedirs("data", exist_ok=True)

    with open("data/transactions.txt", "a") as f:
        f.write(f"{coin.upper()} TX: {url}\n")

