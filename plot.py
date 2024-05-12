import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from preprocess import resample, calc_macd, calc_bollinger

pio.templates.default = "plotly_dark"


def make_fig(df, rule):
    tmp_df = resample(rule)
    tmp_df, gc, dc = calc_macd(tmp_df)
    tmp_df = calc_bollinger(tmp_df)

    layout = {
        "hight": 1000,
        "title": f"BitFlyer FX | {rule}",
        "xaxis": {"title": "Date", "rangeslider": {"visible": False}},
        "yaxis1": {"title": "Price[¥]", "side": "left", "tickformat": ",", "domain": [.45, 1.0]},
        "yaxis2": {"domain": [.45, .45]},
        "yaxis3": {"domain": [.30, .45], "title": "Volume", "side": "right"},
        "yaxis4": {"domain": [.00, .30], "title": "MACD", "side": "right"},
    }

    data = [
        go.Candlestick(
            x=tmp_df.index,
            open=tmp_df.open,
            high=tmp_df.high,
            low=tmp_df.low,
            close=tmp_df.close,
            yaxis="y1"
        ),
        go.Scatter(
            x=gc.index,
            y=gc.close,
            name="Golden Cross",
            opacity=0.8,
            mode="markers",
            marker={"size": 12, "color": "red", "symbol": "triangle-up"},
            yaxis="y1"
        ),
        go.Scatter(
            x=dc.index,
            y=dc.close,
            name="Dead Cross",
            opacity=0.8,
            mode="markers",
            marker={"size": 12, "color": "cyan", "symbol": "triangle-down"},
            yaxis="y1"
        ),
        go.Scatter(
            x=tmp_df.index,
            y=tmp_df.bol_up2sigma,
            name="",
            line={"width": .5, "color": "blue"},
            yaxis="y1"
        ),
        go.Scatter(
            x=tmp_df.index,
            y=tmp_df.bol_down2sigma,
            name="BB", 
            line={"width": .5, "color": "blue"},
            fill="tonexty",
            fillcolor="rgba(0, 0, 255, 0.2)",
            yaxis="y1"
        ),
        go.Scatter(
            x=tmp_df.index,
            y=tmp_df.MA,
            name="MA25",
            line={"color": "pink", "width": 1},
            yaxis="y1"
        ),
        go.Bar(
            x=tmp_df.index,
            y=tmp_df.volumeto,
            name="Volume",
            marker={"color": "rgb(136, 204, 238)"},
            yaxis="y3"
        ),
        go.Scatter(
            x=tmp_df.index,
            y=tmp_df.MACD,
            name="MACD",
            yaxis="y4",
            line={"color": "blue"}
        ),
        go.Scatter(
            x=tmp_df.index,
            y=tmp_df.Signal,
            name="Signal",
            yaxis="y4",
            line={"color": "red"}
        ),
        go.Bar(
            x=tmp_df.index,
            y=tmp_df.Histogram,
            name="Histogram",
            yaxis="y4",
            marker={"color": "green"}
        )
    ]

    fig = go.Figure(data=data, layout=go.Layout(layout))

    return fig