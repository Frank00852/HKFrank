import yfinance as yf
import time
from datetime import datetime

def get_hk_stock_price(stock_c):
    """
    获取港股最新收盘价
    支持输入: 700, 0700, 0700.HK, 00700
    """
    s = str(stock_c).upper().replace(".HK", "").strip()
    s = s.zfill(4)
    ticker = f"{s}.HK"
    try:
        # 只取1天数据，速度最快
        data = yf.Ticker(ticker).history(period="1d")
        if data.empty:
            return {"code": s, "ticker": ticker, "price": None, "msg": "没取到数据"}
        price = float(data["Close"].dropna().iloc[-1])
        return {"code": s, "ticker": ticker, "price": price, "msg": "ok"}
    except Exception as e:
        return {"code": s, "ticker": ticker, "price": None, "msg": f"出错: {e}"}

if __name__ == "__main__":
    # 你关注的港股列表
    watch_list = {
        "0700": "腾讯控股",
        "0001": "长和",
        "0388": "港交所",
        "1299": "友邦保险",
        "0941": "中国移动"
    }

    print(f"--- 港股行情 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    for code, name in watch_list.items():
        result = get_hk_stock_price(code)
        if result["price"]:
            print(f"{code} {name}: {result['price']}")
        else:
            print(f"{code} {name}: {result['msg']}")
    
    # 如果你想做成监控版，取消下面注释，每60秒刷新一次
    # while True:
    #     for code, name in watch_list.items():
    #         print(f"{code} {name}: {get_hk_stock_price(code)['price']}")
    #     print("--- 休眠60秒 ---\n")
    #     time.sleep(60)