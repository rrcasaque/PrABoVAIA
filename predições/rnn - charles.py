# importar as bibliotecas
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import ta
from datetime import datetime
from ta.utils import dropna
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf

# Constantes com as informações ds ações das empresas (TICKET) delimitndo a data de ínicio e fim.
TICKET = '^BVSP'
#TICKET = '^DJI'
#TICKET = 'PETR4.SA' 
#TICKET = 'MSFT'
START = datetime.strptime('2017-11-01', '%Y-%m-%d') 
END = datetime.strptime('2022-11-01', '%Y-%m-%d')

# Obter a cotação das ações da empresa

dataPrice = pd.read_json('resposta.json')
dataPrice = pd.DataFrame(dataPrice.historicalDataPrice[0])
dataPrice.date = pd.to_datetime(dataPrice['date'], unit='s')

#Index(['Open', 'High', 'low', 'close', 'Adj Close', 'Volume']
#Index(['date', 'open', 'high', 'low', 'close', 'volume', 'adjustedClose'], dtype='object')

# Criado um novo data frame apenas com o preço de fechamento e converta-o em um array.
# Cria um novo dataframe apenas com os dados da coluna 'close' da série histórica

data = dataPrice.filter(['close'])
#data = dataPrice.filter(['RSI'])
#data = dataPrice.filter(['MACD'])

# Em seguida, é criado uma variável para armazenar o comprimento do conjunto de dados de treinamento.
# Convertendo o dataframe em um array nump
dataset = data.values
# Obtendo o número de linhas para treinar o modelo 
# É delimitado que o conjunto de dados de treinamento contenha cerca de 80% dos dados.
training_data_len = math.ceil(len(dataset)*.8)
training_data_len 

# Agora dimensione o conjunto de dados para valores entre 0 e 1 inclusive, 
# Geralmente é uma boa prática dimensionar seus dados antes de fornecê-los à rede neural.
# Escala todos os dados para valores entre 0 e 1 
scaler = MinMaxScaler(feature_range=(0, 1)) 
scaled_data = scaler.fit_transform(dataset)

# Crie um conjunto de dados de treinamento que contenha os valores do preço de fechamento dos últimos 60 dias que queremos usar para prever o valor do preço de fechamento do 61º.

# Portanto, a primeira coluna no conjunto de dados ' x_train ' conterá valores do conjunto de dados do índice 0 ao índice 59 (60 valores no total) 
# e a segunda coluna conterá valores do conjunto de dados do índice 1 ao índice 60 (60 valores) e assim por diante.

# O conjunto de dados ' y_train ' conterá o 61º valor localizado no índice 60 para sua primeira coluna e o 62º valor localizado no índice 61 do conjunto de dados 
# para seu segundo valor e assim por diante.

# Cria o conjunto de dados de treinamento dimensionado
train_data = scaled_data[0:training_data_len  , : ]
# Divida os dados em conjuntos de dados x_train e y_train
x_train=[]
y_train = []
for i in range(60,len(train_data)):
    x_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])

# Agora converta o conjunto de dados de trem independente ' x_train ' e o conjunto de dados de trem dependente ' y_train ' em matrizes numpy 
# para que possam ser usados ​​para treinar o modelo LSTM.
# Converter x_train e y_train em arrays numpy
x_train, y_train = np.array(x_train), np.array(y_train)

# Remodele os dados para serem tridimensionais na forma [número de amostras , número de etapas de tempo e número de recursos ]. 
# O modelo LSTM está esperando um conjunto de dados tridimensional.
# Remodele os dados na forma aceita pelo LSTM
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# Construa o modelo LSTM para ter duas camadas LSTM com 50 neurônios e duas camadas Densas, uma com 25 neurônios e outra com 1 neurônio.
# Construa o modelo de rede LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))
model.summary()

# Compile o modelo usando a função de perda de erro quadrático médio (MSE) e o otimizador de adam.
# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Treine o modelo usando os conjuntos de dados de treinamento. Observe que ajuste é outro nome para trem. 
# O tamanho do lote é o número total de exemplos de treinamento presentes em um único lote e a época é o número de iterações 
# quando um conjunto de dados inteiro é passado para frente e para trás pela rede neural.
# Treine o modelo
model.fit(x_train, y_train, batch_size=32, epochs=100)#testar com 100

# Crie um conjunto de dados de teste.
# Teste conjunto de dados
test_data = scaled_data[training_data_len - 60:,:]

# Cria os conjuntos de dados x_test e y_test
x_test = []
y_test =  dataset[training_data_len :,: ] #Obtém todas as linhas do índice 1603 para o resto e todas as colunas (neste caso é apenas a coluna 'close'), então 2003 - 1603 = 400 linhas de dados
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])

# Em seguida, converta o conjunto de dados de teste independente ' x_test ' em uma matriz numpy para que possa ser usado para testar o modelo LSTM.
# Converter x_test em um array numpy
x_test = np.array(x_test)

# Remodele os dados para serem tridimensionais na forma [número de amostras , número de etapas de tempo e número de recursos ]. 
# Isso precisa ser feito, porque o modelo LSTM está esperando um conjunto de dados tridimensional.
# Remodele os dados na forma aceita pelo LSTM
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

# Agora obtenha os valores previstos do modelo usando os dados de teste.
# Obtendo os modelos de valores de preço previstos
predictions = model.predict(x_test) 
predictions = scaler.inverse_transform(predictions)#Desfazer dimensionamento

# Obtenha o erro quadrático médio (RMSE), que é uma boa medida da precisão do modelo. 
# Um valor de 0 indicaria que os valores previstos do modelo correspondem perfeitamente aos valores reais do conjunto de dados de teste.
# Quanto menor o valor, melhor o desempenho do modelo. Mas geralmente é melhor usar outras métricas também para realmente ter uma ideia do desempenho do modelo.
# Calcular/Obter o valor de RMSE
rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
rmse

# Cria os dados para o gráfico
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

# Visualização dos dados da série histórica e do valor previsto pela rede LSTM
plt.figure(figsize=(30,15))
plt.title('Model')
plt.xlabel('Período', fontsize=18)
plt.ylabel('Preço de Fechamento', fontsize=18)
plt.plot(train['close'])
plt.plot(valid[['close','Predictions']])
plt.legend(['Valores de Treinamento', 'Valores Reais Válidos', 'Valores Previsto'], loc='upper left',fontsize=(20))
plt.show()

# Visualização dos dados da série histórica e do valor previsto pela rede LSTM
plt.figure(figsize=(30,12))
#plt.title('Model')
plt.xlabel('Período', fontsize=18)
plt.ylabel('Preço de Fechamento', fontsize=18)
plt.plot(valid[['close']],color='black')
plt.plot(valid[['Predictions']],color='blue', linestyle = 'dashdot', linewidth = 2.5)
#plt.plot(predictionsRSI, color = 'black')
plt.legend(['Valores da Série Histórica','Valores Previstos'],loc='upper left',  fontsize=(20))
plt.show()