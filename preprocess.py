import numpy as np


def calc_macd(df):
    tmp_df = df.copy()
    tmp_df["short"] = tmp_df.close.ewm(span=12).mean()
    tmp_df["long"] = tmp_df.close.ewm(span=26).mean()
    tmp_df["MACD"] = tmp_df.short - tmp_df.long
    tmp_df["Signal"] = tmp_df.MACD.ewm(span=9).mean()
    tmp_df["Histogram"] = tmp_df.MACD - tmp_df.Signal
    tmp_df["difference"] = np.sign(tmp_df.Histogram) - np.sign(tmp_df.Histogram.shift())
    gc = tmp_df[tmp_df.difference==2]
    dc = tmp_df[tmp_df.difference==-2]
    return tmp_df, gc, dc


def calc_bollinger(df):
    tmp_df = df.copy()
    window = 25
    tmp_df["MA"] = tmp_df.close.rolling(window).mean()
    tmp_df["std"] = tmp_df.close.rolling(window).std()
    tmp_df["bol_up2sigma"] = tmp_df.MA + (2 * tmp_df["std"])
    tmp_df["bol_down3sigma"] = tmp_df.MA - (2 * tmp_df["std"])
    return tmp_df


def resample(df, rule):
    tmp_df = df.resample(rule=rule)
    tmp_df = tmp_df.aggregate({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volumeto": "sum",
        "volumefrom": "sum"
    })
    return tmp_df