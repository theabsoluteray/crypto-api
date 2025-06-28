import os
import requests
from dotenv import load_dotenv
from litecoinutils.setup import setup
from litecoinutils.keys import PrivateKey
from litecoinutils.transactions import Transaction, TxInput, TxOutput
from litecoinutils.utils import to_satoshis

from .config import LTC_STATIC_FEE  

load_dotenv()
setup('mainnet')

NOWNODES_API_KEY = os.getenv("NOWNODES_API_KEY")
NOWNODES_BASE_URL = f"https://ltc.nownodes.io/api"

HEADERS = {
    "api-key": NOWNODES_API_KEY
}

def create_wallet():
    priv = PrivateKey()
    address = priv.get_public_key().get_address().to_string()
    return {
        "address": address,
        "private_key": priv.to_wif()
    }

def get_balance(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    res = requests.get(url)

    if res.status_code != 200:
        return {"error": f"BlockCypher error: {res.status_code} - {res.text}"}

    try:
        data = res.json()
        balance_litoshi = data.get("final_balance", 0)  # in litoshi (1 LTC = 100,000,000 litoshi)
        return {"balance": balance_litoshi / 1e8}
    except Exception as e:
        return {"error": f"JSON decode error: {str(e)}"}


def send_ltc(private_key, to_address, amount):
    try:
        priv = PrivateKey(wif=private_key)
        from_address = priv.get_public_key().get_address().to_string()

      
        utxo_url = f"{NOWNODES_BASE_URL}/v1/utxo/{from_address}"
        utxos = requests.get(utxo_url, headers=HEADERS).json()

        inputs = []
        total_input = 0

        for utxo in utxos:
            txid = utxo["txid"]
            vout = utxo["vout"]
            value = float(utxo["value"])
            total_input += value
            inputs.append(TxInput(txid, vout))
            if total_input >= amount + LTC_STATIC_FEE:
                break

        if total_input < amount + LTC_STATIC_FEE:
            return "Error: Insufficient funds"

        tx_outputs = [TxOutput(to_satoshis(amount), to_address)]

       
        change = total_input - amount - LTC_STATIC_FEE
        if change > 0:
            change_address = from_address
            tx_outputs.append(TxOutput(to_satoshis(change), change_address))

        tx = Transaction(inputs, tx_outputs)
        for i, txin in enumerate(inputs):
            tx.sign(i, priv)

        raw_tx = tx.serialize()

        # Broadcast
        broadcast_url = f"{NOWNODES_BASE_URL}/v1/sendtx"
        res = requests.post(broadcast_url, headers=HEADERS, json={"hex": raw_tx})
        res_json = res.json()

        if "txid" in res_json:
            return res_json["txid"]
        else:
            return f"Broadcast failed: {res_json}"

    except Exception as e:
        return f"Error: {str(e)}"
