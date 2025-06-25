from bit import Key, network

def create_wallet():
    key = Key()
    return {
        "address": key.address,
        "private_key": key.to_wif()
    }

def get_balance(address):
    return float(network.get_balance(address))  # In BTC

def send_btc(private_key, to_address, amount):
    key = Key(private_key)
    tx_hash = key.send([(to_address, amount, 'btc')])
    return tx_hash
