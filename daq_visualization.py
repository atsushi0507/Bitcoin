import streamlit as st
from bq import BQClient
import pandas as pd
from plot import make_fig
from datetime import datetime


def main():
    st.set_page_config(
        page_title="Bitcoin",
        page_icon=":coin"
    )

    client = BQClient()

    with st.sidebar:
        st.sidebar.header("Config")
        if st.button("Get Data"):
            st.write("Getting data")
            tmp = client.get_min_historical()
            st.dataframe(client.load_data().sort_values(by="timestamp").tail())
            st.dataframe(tmp.tail())
            client.insert_data_to_db()

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
