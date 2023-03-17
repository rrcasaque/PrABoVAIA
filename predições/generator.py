import pandas as pd
import numpy as np

# Gerando preços aleatórios para uma ação
np.random.seed(123)
price = 100
prices = []
for i in range(1000):
    prices.append(price)
    price += np.random.normal(loc=0, scale=1)
    
# Salvando os preços em um arquivo CSV
df = pd.DataFrame({'Price': prices})
df.to_csv('stock_data.csv', index=False)