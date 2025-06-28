from bit import Key, network
from config import BTC_STATIC_FEE
def create_wallet():
    key = Key()
    return {
        "address": key.address,
        "private_key": key.to_wif()
    }

def get_balance(address):
    return float(network.get_balance(address)) 

def send_btc(private_key, to_address, amount):
    try:
        key = Key(private_key)

      
        unspents = key.get_unspents()

        
        balance = sum([utxo.amount for utxo in unspents])
        if balance < amount:
            raise ValueError("Insufficient balance in wallet.")

        fee = BTC_STATIC_FEE
        if amount <= fee:
            raise ValueError("Amount too low to cover network fee.")

        send_amount = amount - fee

      
        tx_hash = key.send([(to_address, send_amount, 'btc')], fee=int(fee * 1e8))
        return tx_hash

    except ValueError as ve:
        return f"ValueError: {str(ve)}"
    
    except Exception as e:
        return f"Error: {str(e)}"
