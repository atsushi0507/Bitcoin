import streamlit as st
from Daq import Daq
import pandas as pd
from plot import make_fig


col1, col2 = st.columns(2)

st.title("Bitcoin")
st.header("Bit coin")


with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

    if st.button("Get Data"):
        st.write("Getting data")

with col2:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

    rule_option = st.selectbox(
        "ローソク足の選択",
        [
            "1min",
            "5min",
            "15min",
            "1h",
            "4h"
            "1d"
        ]
    )

    daq = Daq()
    df  = daq.read_data_from_db()

    df["timestamp"] = pd.to_datetime(df.timestamp)
    df = df.set_index("timestamp")

    if rule_option is not None:
        fig = make_fig(df, rule="15min")
        st.plotly_chart(fig, use_container_width=True)