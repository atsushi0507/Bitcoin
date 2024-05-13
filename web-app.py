import streamlit as st
from Daq import Daq
import pandas as pd
from plot import make_fig


def main():
    st.set_page_config(
        page_title="Bitcoin",
        page_icon=":shark"
    )

    daq = Daq()

    with st.sidebar:
        st.sidebar.header("Config")
        if st.button("Get Data"):
            st.write("Getting data")
            ohlc_data = daq.get_min_historical()
            daq.insert_data_to_db(ohlc_data)
            st.dataframe(daq.read_data_from_db().tail(10))

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

    df = daq.read_data_from_db()

    df["timestamp"] = pd.to_datetime(df.timestamp)
    df = df.set_index("timestamp")

    if rule_option is not None:
        fig = make_fig(df, rule=rule_option)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
