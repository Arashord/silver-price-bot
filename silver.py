import requests
import os
import json

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
PRICE_FILE = 'last_price.json'
API_URL = 'https://webapi.charisma.ir/api/Plan/plan-calculator-info-by-id?planId=04689a46-3eff-45d4-a070-f83f7d4d20d8'

def get_price():
    r = requests.get(API_URL, timeout=10)
    data = r.json()
    return data['lastPrice']

def send_telegram(msg):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'})

def load_last_price():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE) as f:
            return json.load(f)['price']
    return None

def save_price(price):
    with open(PRICE_FILE, 'w') as f:
        json.dump({'price': price}, f)

current = get_price()
last = load_last_price()

if last is None:
    save_price(current)
    send_telegram(f'🚀 ربات نقره فعال شد!\n💰 قیمت فعلی: <b>{current:,}</b> تومان')
elif current != last:
    diff = current - last
    emoji = '📈' if diff > 0 else '📉'
    msg = f'{emoji} تغییر قیمت نقره\n\nقبلی: {last:,}\nجدید: <b>{current:,}</b>\nتفاوت: {diff:+,} تومان'
    send_telegram(msg)
    save_price(current)
else:
    print(f'No change: {current}')
