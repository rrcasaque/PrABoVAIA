import pandas as pd
import matplotlib.pyplot as plt
  
stock_prices = pd.read_json('resposta.json')

stock_prices = pd.DataFrame(stock_prices.historicalDataPrice[0])

stock_prices.date = pd.to_datetime(stock_prices['date'], unit='s')

plt.figure()
  
up = stock_prices[stock_prices.close >= stock_prices.open]
  
down = stock_prices[stock_prices.close < stock_prices.open]
  
col1 = 'green'
  
col2 = 'red'
  
width = .3
width2 = .03
  
plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=col1)
plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color=col1)
plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=col1)
  
plt.bar(down.index, down.close-down.open, width, bottom=down.open, color=col2)
plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color=col2)
plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color=col2)
  
plt.xticks(rotation=30, ha='right')
plt.title('MXRF11 - History of price')
plt.show()