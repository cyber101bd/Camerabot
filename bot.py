import yfinance as yf
import pandas_ta as ta
from telegram import Bot
import asyncio
import time

# --- কনফিগারেশন (আপনার তথ্য এখানে দিন) ---
TOKEN = '8638174442:AAElpuOCU8iHqOIPcacBBOgPlaxoEulSepk' # BotFather থেকে পাওয়া টোকেন
CHAT_ID = '6264050385'           # আপনার টেলিগ্রাম আইডি
SYMBOL = 'EURUSD=X'                # যে পেয়ারে সিগন্যাল চান (যেমন: EURUSD, GBPUSD)
TIMEFRAME = '1m'                   # ১ মিনিটের চার্ট (1m, 5m, 15m)

async def send_telegram_msg(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def get_signal():
    # ১. লাইভ মার্কেট ডেটা ডাউনলোড (রিয়েল-টাইম)
    data = yf.download(SYMBOL, period='1d', interval=TIMEFRAME, progress=False)
    
    if data.empty:
        return None

    # ২. টেকনিক্যাল ইন্ডিকেটর ক্যালকুলেশন
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    
    current_price = last_row['Close']
    rsi_val = last_row['RSI']
    ema_val = last_row['EMA_20']

    # ৩. সিগন্যাল লজিক (AI Strategy)
    signal = None
    
    # BUY কন্ডিশন: RSI ৩০ এর নিচে (Oversold) এবং প্রাইস EMA এর উপরে যাচ্ছে
    if rsi_val < 35 and current_price > ema_val:
        signal = f"🟢 BUY (UP) \nPair: {SYMBOL} \nPrice: {current_price:.5f} \nRSI: {rsi_val:.2f}"
    
    # SELL কন্ডিশন: RSI ৭০ এর উপরে (Overbought) এবং প্রাইস EMA এর নিচে যাচ্ছে
    elif rsi_val > 65 and current_price < ema_val:
        signal = f"🔴 SELL (DOWN) \nPair: {SYMBOL} \nPrice: {current_price:.5f} \nRSI: {rsi_val:.2f}"
        
    return signal

async def main():
    print(f"🚀 Bot Started for {SYMBOL}...")
    last_signal_time = None

    while True:
        try:
            signal = get_signal()
            
            # একই ক্যান্ডেলে বারবার সিগন্যাল পাঠানো বন্ধ করতে
            current_time = time.strftime("%H:%M")
            
            if signal and last_signal_time != current_time:
                print(f"New Signal Found at {current_time}!")
                await send_telegram_msg(f"⏰ Time: {current_time}\n{signal}")
                last_signal_time = current_time
            
            # প্রতি ১০ সেকেন্ড পর পর মার্কেট চেক করবে
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
