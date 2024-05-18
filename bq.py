from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
import requests
from datetime import datetime
import streamlit as st


class BQClient:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.project_id = credentials.project_id
        self.client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )
        self.base_url = "https://min-api.cryptocompare.com/data/v2"
        self.api_key = st.secrets["CRYPTO_COMPARE_API_KEY"]["key"]

    def load_data(self):
        query = """
            SELECT
                *
            FROM
                `crypto-asset-fx.bitflyer.bitcoin_jpy`
            ORDER BY
                timestamp DESC
            """
        self.bq_df = self.client.query(query).to_dataframe()
        self.bq_df["timestamp"] = pd.to_datetime(self.bq_df.timestamp)# .dt.tz_convert("Asia/Tokyo")
        return self.bq_df
    
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
            use_cols = [
                "timestamp", "open", "high", "low", "close",
                "volumeto", "volumefrom"
            ]
            df = pd.DataFrame(data)
            df["timestamp"] = df["time"].apply(lambda x: datetime.fromtimestamp(int(x)).strftime("%Y-%m-%d %H:%M:%S"))
            df["timestamp"] = pd.to_datetime(df.timestamp, utc=True)# .dt.tz_convert("Asia/Tokyo")
            self.df = df[use_cols]
            return self.df
        else:
            return None
        
    def insert_data_to_db(self):
        self.load_data()
        self.unique_df = self.df[~self.df.set_index("timestamp").index.isin(self.bq_df.set_index("timestamp").index)]
        st.dataframe(self.unique_df)

        if not self.unique_df.empty:
            # self.unique_df.to_gbq(
            #     destination_table="bitflyer.bitcoin_jpy",
            #     project_id=self.project_id,
            #     if_exists="append"
            # )
            try:
                pandas_gbq.to_gbq(
                    dataframe=self.unique_df,
                    destination_table="bitflyer.bitcoin_jpy",
                    project_id=self.project_id,
                    if_exists="append"
                )
            except Exception as e:
                st.error(f"Error  inserting data: {e}")
        else:
            print("差分はありません")