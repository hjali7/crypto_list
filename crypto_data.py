import requests
from dotenv import load_dotenv
import os

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()
print("بارگذاری فایل .env انجام شد.")

# خواندن کلید API از متغیرهای محیطی
CMC_API_KEY = os.getenv("CMC_API_KEY")
if not CMC_API_KEY:
    print("خطا: CMC_API_KEY در فایل .env تعریف نشده است!")
else:
    print("کلید API CoinMarketCap با موفقیت بارگذاری شد.")

crypto_data = []
current_service = "coingecko"  # سرویس پیش‌فرض

def fetch_and_store_data(service="coingecko"):
    global crypto_data, current_service
    current_service = service
    print(f"در حال دریافت داده‌ها از {service}...")

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
            response = requests.get(url, params=params, timeout=10)
            print(f"وضعیت پاسخ CoinGecko: {response.status_code}")
            if response.status_code == 200:
                crypto_data = response.json()
                print(f"داده‌ها از CoinGecko دریافت شد. تعداد: {len(crypto_data)}")
                return True
            else:
                print(f"خطا در CoinGecko: کد {response.status_code}")
                return False
        except Exception as e:
            print(f"خطا در اتصال به CoinGecko: {str(e)}")
            return False

    elif service == "coinmarketcap":
        if not CMC_API_KEY:
            print("خطا: کلید API CoinMarketCap موجود نیست!")
            return False
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CMC_API_KEY,
        }
        params = {
            'start': 1,
            'limit': 100,
            'convert': 'USD'
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"وضعیت پاسخ CoinMarketCap: {response.status_code}")
            if response.status_code == 200:
                data = response.json()['data']
                crypto_data = [
                    {
                        'name': coin['name'],
                        'current_price': coin['quote']['USD']['price'],
                        'image': f"https://s2.coinmarketcap.com/static/img/coins/64x64/{coin['id']}.png"
                    }
                    for coin in data
                ]
                print(f"داده‌ها از CoinMarketCap دریافت شد. تعداد: {len(crypto_data)}")
                return True
            else:
                print(f"خطا در CoinMarketCap: کد {response.status_code}")
                return False
        except Exception as e:
            print(f"خطا در اتصال به CoinMarketCap: {str(e)}")
            return False

    return False

def get_crypto_data():
    return crypto_data

def get_current_service():
    return current_service