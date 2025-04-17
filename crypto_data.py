import requests

# کلید API برای CoinMarketCap
CMC_API_KEY = "YOUR_COINMARKETCAP_API_KEY"  # اینجا کلید API خودت رو وارد کن

crypto_data = []
current_service = "coingecko"  # سرویس پیش‌فرض

def fetch_and_store_data(service="coingecko"):
    global crypto_data, current_service
    current_service = service

    if service == "coingecko":
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': False
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                crypto_data = response.json()
                return True
            else:
                return False
        except:
            return False

    elif service == "coinmarketcap":
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY':" aed31ae5-ff4b-4428-899b-2ce78a284569",
        }
        params = {
            'start': 1,
            'limit': 100,
            'convert': 'USD'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()['data']
                # تبدیل فرمت داده‌ها به فرمت مشابه CoinGecko
                crypto_data = [
                    {
                        'name': coin['name'],
                        'current_price': coin['quote']['USD']['price'],
                        'image': f"https://s2.coinmarketcap.com/static/img/coins/64x64/{coin['id']}.png"
                    }
                    for coin in data
                ]
                return True
            else:
                return False
        except:
            return False

    return False

def get_crypto_data():
    return crypto_data

def get_current_service():
    return current_service