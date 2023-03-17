from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_json('resposta.json')

df = pd.DataFrame(df.historicalDataPrice[0])

df.date = pd.to_datetime(df['date'], unit='s')

print(df.columns)

# plt.plot(df.date, df.close, color='orange' )
# plt.title('MXRF11 - History of price')
# plt.show()