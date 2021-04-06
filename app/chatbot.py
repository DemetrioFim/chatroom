import pandas as pd

def get_stock(data):
    if data.startswith('/stock='):
        try:
            share = data.split('/stock=')[1].strip()
            url = f'https://stooq.com/q/l/?s={share.lower()}&f=sd2t2ohlcv&h&e=csv'
            df = pd.read_csv(url)
            price = float(df['Close'].values[0])
            msg = f"{share.upper()} quote is ${price} per share"
        except Exception as e:
            print(e)
            msg = "Share not found!"
        return msg
