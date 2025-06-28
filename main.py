from flask import Flask, request, jsonify , send_file
from services import eth, btc, ltc, price
from dotenv import load_dotenv 
from services.utils import save_wallet , log_transaction
import os, json ,csv

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



@app.route('/export-wallets', methods=['GET'])
def export_wallets():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No wallet data found"}), 404

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    export_file = 'data/exported_wallets.csv'
    os.makedirs(os.path.dirname(export_file), exist_ok=True)

    with open(export_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['coin', 'address', 'private_key'])
        writer.writeheader()

        for coin, wallets in data.items():
            for w in wallets:
                writer.writerow({
                    'coin': coin,
                    'address': w['address'],
                    'private_key': w['private_key']
                })

    return send_file(export_file, as_attachment=True)
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
def send(coin):
    data = request.get_json()
    from_addr = data.get("from_address")
    to_addr = data.get("to_address")
    amount = data.get("amount")

    private_key = find_private_key(coin, from_addr)
    if not private_key:
        return jsonify({"error": "Wallet not found"}), 404

  
    if coin == "btc":
        txid = btc.send_transaction(from_addr, to_addr, amount, private_key)
    elif coin == "eth":
        txid = eth.send_transaction(from_addr, to_addr, amount, private_key)
    elif coin == "ltc":
        txid = ltc.send_transaction(from_addr, to_addr, amount, private_key)
    else:
        return jsonify({"error": "Unsupported coin"}), 400

   
    log_transaction(coin, txid)

    return jsonify({
        "message": "Transaction sent",
        "txid": txid,
        "explorer": f"{coin.upper()} TX: logged in transactions.txt"
    })

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()
    coin = data.get("coin")
    address = data.get("address")

    if not coin or not address:
        return jsonify({"error": "coin and address are required"}), 400

    try:
        if coin == "eth":
            balance = eth.get_balance(address)

        elif coin == "btc":
            balance = btc.get_balance(address)

        elif coin == "ltc":
            balance = ltc.get_balance(address)

        else:
            return jsonify({"error": f"{coin.upper()} not supported"}), 400

        return jsonify({
            "status": "success",
            "coin": coin.upper(),
            "address": address,
            "balance": str(balance)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/price/<coin>')
def get_price(coin):
    return jsonify({'usd': price.get_price(coin)})

if __name__ == '__main__':
    app.run(debug=True)
