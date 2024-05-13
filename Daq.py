import sqlite3
import requests
from datetime import datetime
import os
import pandas as pd


class Daq:
    def __init__(self):
        self.conn = sqlite3.connect("bitflyer.db")
        self.c = self.conn.cursor()
        self.base_url = "https://min-api.cryptocompare.com/data/v2"
        self.create_table()
        self.api_key = os.environ["CRYPTO_COMPARE_API_KEY"]

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS ohlc
                       (id INTEGER PRIMARY KEY,
                       timestamp DATETIME,
                       open FLOAT,
                       high FLOAT,
                       low FLOAT,
                       close FLOAT,
                       volumefrom FLOAT,
                       volumeto FLOAT)''')
        self.conn.commit()

    def get_min_historical(self):
        url = self.base_url + "/histominute"
        params = {
            "fsym": "BTC",
            "tsym": "JPY",
            "limit": 2000,
            "e": "bitFlyerFX",
            "api_key": self.api_key
        }
        response = requests.get(url, params)
        if response.status_code == 200:
            data = response.json()["Data"]["Data"]
            return data
        else:
            print("Error fetching data from CryptoCompare API")
            return None

    def insert_data_to_db(self, data):
        if data:
            for candle in data:
                timestamp = datetime.fromtimestamp(candle["time"]).strftime("%Y-%m-%d %H:%M:%S")
                open_price = float(candle["open"])
                high_price = float(candle["high"])
                low_price = float(candle["low"])
                close_price = float(candle["high"])
                volume_to = float(candle["volumeto"])
                volume_from = float(candle["volumefrom"])

                # 重複データがある場合はスキップ
                self.c.execute('''SELECT * FROM ohlc WHERE timestamp = ?''', (timestamp,))
                if not self.c.fetchone():
                    self.c.execute('''INSERT INTO ohlc (timestamp, open, high, low, close, volumeto, volumefrom)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''', (timestamp, open_price, high_price, low_price, close_price, volume_to, volume_from))
            self.conn.commit()
            print("Data inserted successfully.")
        else:
            print("No data to insert")

    def read_data_from_db(self, start=None, end=None):
        if not (start and end):
            return pd.read_sql("""SELECT open, high, low, close, volumeto, volumefrom, timestamp FROM ohlc ORDER BY timestamp""", self.conn)
        else:
            if (start or end) is None:
                print("If you want to set date range, you need to specify both of start and end")
            else:
                return pd.read_sql(f"""SELECT open, high, low, close, volumeto, volumefrom, timestamp FROM ohlc WHERE timestamp >= '{start}' AND timestamp <= '{end}' ORDER BY timestamp""", self.conn)


if __name__ == "__main__":
    daq = Daq()
    ohlc_data = daq.get_min_historical()
    daq.insert_data_to_db(ohlc_data)
