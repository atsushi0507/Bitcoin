import streamlit as st
from Daq import Daq
from bq import BQClient
import pandas as pd
from plot import make_fig
from datetime import datetime


def main():
    st.set_page_config(
        page_title="Bitcoin",
        page_icon=":coin"
    )

    daq = Daq()
    client = BQClient(st.secrets["gcp_project_id"])

    with st.sidebar:
        st.sidebar.header("Config")
        if st.button("Get Data"):
            st.write("Getting data")
            #ohlc_data = daq.get_min_historical()
            _ = client.get_min_historical()
            client.insert_data_to_db()
            st.dataframe(client.unique_df.sort_values("timestamp").tail(10))

        rule_option = st.selectbox(
            "ローソク足の選択",
            [
                "1min",
                "5min",
                "15min",
                "1h",
                "4h",
                "1d"
            ]
        )

        today = datetime.today()
        today_str = f"{today.year}-{today.month}-{today.day}"
        with open("bitflyer.db", "rb") as f:
            db_bytes = f.read()
        st.download_button(
            label="DBファイルをダウンロードする",
            data=db_bytes,
            file_name=f"bitflyer_{today_str}.db",
            mime="application/octet-stream"
        )

    df = client.load_data()

    df["timestamp"] = pd.to_datetime(df.timestamp, utc=True).dt.tz_convert("Asia/Tokyo")
    df = df.set_index("timestamp")

    if rule_option is not None:
        fig = make_fig(df, rule=rule_option)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
