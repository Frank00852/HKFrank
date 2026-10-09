import yfinance as yf
import pandas as pd
from datetime import datetime

WATCH_LIST = [
    ("0700.HK", "腾讯控股"),
    ("9988.HK", "阿里巴巴"),
    ("3690.HK", "美团"),
    ("9618.HK", "京东集团"),
    ("1024.HK", "快手"),
    ("1211.HK", "比亚迪"),
    ("1810.HK", "小米集团"),
    ("0005.HK", "汇丰控股"),
    ("0941.HK", "中国移动"),
    ("0883.HK", "中海油"),
    ("1299.HK", "友邦保险"),
    ("0388.HK", "港交所"),
    ("2318.HK", "中国平安"),
    ("2015.HK", "理想汽车"),
    ("9868.HK", "小鹏汽车"),
    ("9999.HK", "网易"),
    ("2800.HK", "盈富基金"),
    ("0700.HK", "南方恒生科技"),
    ("0700.HK", "Placeholder"),
    ("0700.HK", "Placeholder2"),
]
# 去重并保留20只
seen = set()
WATCH_LIST_UNIQUE = []
for code, name in WATCH_LIST:
    if code not in seen:
        WATCH_LIST_UNIQUE.append((code, name))
        seen.add(code)
# 补齐18只真实 + 2个备用
WATCH_LIST_UNIQUE = [
    ("0700.HK", "腾讯控股"),
    ("9988.HK", "阿里巴巴"),
    ("3690.HK", "美团"),
    ("9618.HK", "京东集团"),
    ("1024.HK", "快手"),
    ("1211.HK", "比亚迪"),
    ("1810.HK", "小米"),
    ("0005.HK", "汇丰控股"),
    ("0941.HK", "中国移动"),
    ("0883.HK", "中海油"),
    ("1299.HK", "友邦"),
    ("0388.HK", "港交所"),
    ("2318.HK", "中国平安"),
    ("2015.HK", "理想"),
    ("9868.HK", "小鹏"),
    ("9999.HK", "网易"),
    ("2800.HK", "盈富基金"),
    ("3008.HK", "南方恒科ETF"),
]

def fetch_one(code, name):
    try:
        ticker = yf.Ticker(code)
        hist = ticker.history(period="5d")  # 取5天，防止2天不够
        if hist.empty or len(hist) < 1:
            return {"代码": code, "名称": name, "现价": 0.0, "涨跌": 0.0, "涨跌幅%": 0.0, "状态": "无数据"}

        last = float(hist['Close'].iloc[-1])
        prev = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else last
        
        change = last - prev
        pct = (change / prev * 100) if prev != 0 else 0.0

        return {
            "代码": code,
            "名称": name,
            "现价": round(last, 3),
            "涨跌": round(change, 3),
            "涨跌幅%": round(pct, 2),
            "状态": "OK"
        }
    except Exception as e:
        return {"代码": code, "名称": name, "现价": 0.0, "涨跌": 0.0, "涨跌幅%": 0.0, "状态": f"失败:{str(e)[:15]}"}

def fetch_once():
    rows = []
    for code, name in WATCH_LIST_UNIQUE:
        rows.append(fetch_one(code, name))
    
    df = pd.DataFrame(rows)
    # 确保全是数字，才能排序，不会再报错
    df["涨跌幅%"] = pd.to_numeric(df["涨跌幅%"], errors="coerce").fillna(0.0)
    df = df.sort_values("涨跌幅%", ascending=False)
    return df

if __name__ == "__main__":
    print(f"=== HKFrank v3.1 港股监控 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    df = fetch_once()
    
    # 只显示成功的
    df_ok = df[df["状态"] == "OK"]

    try:
        from tabulate import tabulate
        print(tabulate(df_ok, headers='keys', tablefmt='psql', showindex=False))
        if len(df) != len(df_ok):
            print("\n部分抓取失败：")
            print(tabulate(df[df["状态"] != "OK"], headers='keys', tablefmt='plain', showindex=False))
    except ImportError:
        print(df_ok.to_string(index=False))
    
    print(f"\n共抓取 {len(df_ok)}/{len(df)} 只，时间 {datetime.now().strftime('%H:%M:%S')}")
    print("提示：盘外显示为昨日收盘价")