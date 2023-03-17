import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# carrega os dados históricos dos preços das ações da Apple

df = pd.read_json('resposta.json')

df = pd.DataFrame(df.historicalDataPrice[0])

df.date = pd.to_datetime(df['date'], unit='s')

# data = pd.read_csv('predições/AAPL.csv')
data = df['close'].values.reshape(-1, 1)

# normaliza os dados entre 0 e 1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

# divide os dados em conjuntos de treinamento e teste
train_size = int(len(data) * 0.8)
test_size = len(data) - train_size
train_data, test_data = data[0:train_size,:], data[train_size:len(data),:]

# converte os dados em sequências de entrada e saída para treinamento da RNN
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

look_back = 30
train_X, train_Y = create_dataset(train_data, look_back)
test_X, test_Y = create_dataset(test_data, look_back)

# define a arquitetura da rede LSTM
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(50, input_shape=(look_back, 1)))
model.add(tf.keras.layers.Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# treina a rede LSTM
history = model.fit(train_X, train_Y, epochs=100, batch_size=1, verbose=2)

# faz a previsão dos preços das ações para o conjunto de teste
test_predict = model.predict(test_X)

# converte as previsões para a escala original
test_predict = scaler.inverse_transform(test_predict)
test_Y = scaler.inverse_transform([test_Y])

# calcula o erro médio quadrático (MSE) da previsão
mse = np.mean((test_predict - test_Y)**2)
print(f'MSE: {mse:.2f}')

# plota o resultado da previsão
plt.plot(test_Y.flatten(), label='Dados reais')
plt.plot(test_predict.flatten(), label='Previsão')
plt.legend('Previsão de valores MXRF11')
plt.show()