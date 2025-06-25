from flask import Flask, request, jsonify
from services import eth, btc, ltc, price
from dotenv import load_dotenv
from services.utils import save_wallet
import os, json

load_dotenv()
app = Flask(__name__)

DATA_FILE = 'data/wallets.json'

def find_private_key(coin, address):
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        wallets = json.load(f)
    for w in wallets:
        if w['coin'] == coin and w['address'] == address:
            return w['private_key']
    return None

@app.route('/wallet/<coin>')
def create_wallet(coin):
    if coin == 'eth':
        wallet = eth.create_wallet()
    elif coin == 'btc':
        wallet = btc.create_wallet()
    elif coin == 'ltc':
        wallet = ltc.create_wallet()
    else:
        return jsonify({'error': 'Unsupported coin'}), 400

    save_wallet(coin, wallet['address'], wallet['private_key'])
    return jsonify(wallet)

@app.route('/balance/<coin>', methods=['GET'])
def get_balance(coin):
    address = request.args.get('address')
    private_key = find_private_key(coin, address)
    if not private_key:
        return jsonify({'error': 'Wallet not found for given address'}), 404

    if coin == 'eth':
        return jsonify({'balance': eth.get_balance(address)})
    if coin == 'btc':
        return jsonify({'balance': btc.get_balance(address)})
    if coin == 'ltc':
        return jsonify({'balance': ltc.get_balance(address)})
    return jsonify({'error': 'Unsupported coin'}), 400

@app.route('/send/<coin>', methods=['POST'])
def send_coin(coin):
    data = request.json
    from_address = data.get('from_address')
    to_address = data.get('to')
    amount = data.get('amount')
    if not all([from_address, to_address, amount]):
        return jsonify({'error': 'Missing required parameters'}), 400

    private_key = find_private_key(coin, from_address)
    if not private_key:
        return jsonify({'error': 'Wallet not found for given address'}), 404

    if coin == 'eth':
        return jsonify({'tx_hash': eth.send_eth(private_key, to_address, amount)})
    if coin == 'btc':
        return jsonify({'tx_hash': btc.send_btc(private_key, to_address, amount)})
    if coin == 'ltc':
        return jsonify({'tx_hash': ltc.send_ltc(private_key, to_address, amount)})
    return jsonify({'error': 'Unsupported coin'}), 400

@app.route('/price/<coin>')
def get_price(coin):
    return jsonify({'usd': price.get_price(coin)})

if __name__ == '__main__':
    app.run(debug=True)
