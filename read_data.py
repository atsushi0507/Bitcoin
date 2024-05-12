from Daq import Daq

daq = Daq()
df = daq.read_data_from_db()
print(df.tail(10))