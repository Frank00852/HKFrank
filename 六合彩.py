import yfinance as yf

def get_hk_stock_price(stock_c):
    s = str(stock_c).upper().replace(".HK","").strip()
    s = s.zfill(4)
    ticker = f"{s}.HK"
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if data.empty:
            return f"{ticker} 没取到数据"
        return float(data["Close"].dropna().iloc[-1])
    except Exception as e:
        return f"出错: {e}"

if __name__ == "__main__":
    print(get_hk_stock_price("0700"))  # 测腾讯
    print(get_hk_stock_price("0001"))  # 测工商银行