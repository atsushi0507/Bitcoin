from Daq import Daq

daq = Daq()
ohlc_data = daq.get_min_historical()

daq.insert_data_to_db(ohlc_data)
