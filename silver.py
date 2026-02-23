import requests, os, time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_silver_price():
    url = "https://webapi.charisma.ir/api/Plan/plan-calculator-info-by-id?planId=04689a46-3eff-45d4-a070-f83f7d4d20d8"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    return round(r.json()['lastPrice'], 0)

def send_to_telegram(price, old_price=None):
    if old_price:
        change = price - old_price
        emoji = "📈" if change > 0 else "📉"
        msg = f"{emoji} قیمت نقره تغییر کرد!\nقبلی: {old_price:,.0f} تومان\nجدید: {price:,.0f} تومان\nتفاوت: {change:+,.0f} تومان"
    else:
        msg = f"💰 قیمت نقره: {price:,.0f} تومان"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": CHAT_ID, "text": msg})

last_price = None
for i in range(5):
    try:
        price = get_silver_price()
        if price != last_price:
            send_to_telegram(price, last_price)
            last_price = price
    except Exception as e:
        print(f"خطا: {e}")
    if i < 4:
        time.sleep(60)
