import requests

COIN_IDS = {
    'eth': 'ethereum',
    'btc': 'bitcoin',
    'ltc': 'litecoin'
}

def get_price(coin_symbol):
    coin_id = COIN_IDS.get(coin_symbol.lower())
    if not coin_id:
        return 0
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    res = requests.get(url)
    if res.status_code != 200:
        return 0
    return res.json().get(coin_id, {}).get('usd', 0)
