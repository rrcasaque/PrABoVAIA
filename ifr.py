import pandas as pd

df = pd.read_json('resposta.json')

df = pd.DataFrame(df.historicalDataPrice[0])

df.date = pd.to_datetime(df['date'], unit='s')

#IFR = 100 – 100 / ( 1 + FR)
#FR = Média de Ganho / Média de perdas

def getFR(dataframe,opRange,openName,closeName):
    hSum = 0    
    lSum = 0
    hCount = 0
    lCount = 0        
    for i in range(0,opRange-1):        
        if(dataframe[openName][i]>dataframe[closeName][i]):
            hSum += dataframe[openName][i] - dataframe[closeName][i]
            hCount = hCount+1
        else:
            lSum += dataframe[closeName][i] - dataframe[openName][i]
            lCount = lCount+1
    return (hSum/hCount)/(lSum/lCount)

def getIFR(fr):
    return 100 - 100 / (1 + fr)

print(getIFR(getFR(df,14,'open','close')))