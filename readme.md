<div align="center">
  <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png" height="60"/> &nbsp;
  <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png" height="60"/> &nbsp;
  <img src="https://cryptologos.cc/logos/litecoin-ltc-logo.png" height="60"/>

  <h1>💸 Crypto API — Send, Receive & Track in USD</h1>
  <p>A minimal Flask API for Bitcoin, Ethereum, and Litecoin with real-time USD conversion</p>
</div>

---

## ✨ Features

- 📤 Send BTC, ETH, or LTC using private keys
- 📈 Uses real-time prices via [CoinGecko API](https://www.coingecko.com/)
- 🔐 Wallet management (JSON-based)
- 📝 Logs transactions in `transactions.txt`

---

## 📦 Setup

```bash
git clone https://github.com/your-username/crypto-api.git
cd crypto-api
pip install -r ray.txt
cp .example.env .env
# Fill in your API keys in .env
python main.py
```

# structure
```bash

├── main.py
├── services/
│   ├── btc.py
│   ├── eth.py
│   ├── ltc.py
│   ├── convert.py
│   └── price.py
├── data/
│   ├── wallets.json
│   └── transactions.txt
```
