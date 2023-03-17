import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import random

# Função para avaliar a aptidão de cada indivíduo
def evaluate_individual(individual, df):
    # Extraindo os genes do modelo de previsão e da estratégia de negociação
    model_genes = individual[:LOOKBACK_PERIOD+1]
    strategy_genes = individual[LOOKBACK_PERIOD+1:]

    # Criando o modelo de previsão
    model = LinearRegression()
    X = []
    for i in range(LOOKBACK_PERIOD, 0, -1):
        X.append(df.iloc[-i]['Price'])
    X.append(df.iloc[-1]['Price'])
    X = np.array(X).reshape(-1, 1)
    y = np.array(df['Price'][-(LOOKBACK_PERIOD+1):])
    model.fit(X, y)

    # Fazendo a previsão
    X = np.array(df['Price'][-LOOKBACK_PERIOD-1:]).reshape(-1, 1)
    y = np.array(df['Price'][-LOOKBACK_PERIOD:])
    prediction = model.predict(X)[-1]
    if strategy_genes[0] > 0:
        prediction *= (1 + strategy_genes[0])
    else:
        prediction *= (1 - strategy_genes[0])
    if strategy_genes[1] > 0:
        prediction += strategy_genes[1]
    else:
        prediction -= strategy_genes[1]

    # Calculando o erro absoluto da previsão
    actual = df.iloc[-1]['Price']
    error = abs(prediction - actual)

    return 1/error

# Função para avaliar a aptidão de toda a população
def evaluate_population(population, df):
    fitness_scores = []
    for individual in population:
        fitness_scores.append(evaluate_individual(individual, df))
    return fitness_scores

# Função para cruzar dois indivíduos
def crossover(individual_1, individual_2):
    index = random.randint(0, len(individual_1)-1)
    child_1 = np.concatenate((individual_1[:index], individual_2[index:]))
    child_2 = np.concatenate((individual_2[:index], individual_1[index:]))
    return child_1, child_2

# Função para aplicar mutação em um indivíduo
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] += np.random.normal()
    return individual

# Função para evoluir a população para a próxima geração
def evolve_population(population, fitness_scores, mutation_rate):
    new_population = []
    while len(new_population) < len(population):
        candidate_1 = population[random.randint(0, len(population)-1)]
        candidate_2 = population[random.randint(0, len(population)-1)]
        child_1, child_2 = crossover(candidate_1, candidate_2)
        child_1 = mutate(child_1, mutation_rate)
        child_2 = mutate(child_2, mutation_rate)
        new_population.append(child_1)
        new_population.append(child_2)
    return new_population[:len(population)]

# Definindo os hiperparâmetros
LOOKBACK_PERIOD = 30
POPULATION_SIZE = 50
NUM_GENERATIONS = 50
MUTATION_RATE = 0.1

# Carregando os dados

df = pd.read_csv('predições/stock_data.csv')

# Normalizando os preços
df['Price'] = df['Price'] / 100

# Criando a população inicial
population = []
for i in range(POPULATION_SIZE):
    individual = np.concatenate((np.random.normal(size=LOOKBACK_PERIOD+1), np.random.normal(size=2)))
    population.append(individual)

# Evoluindo a população por várias gerações
for i in range(NUM_GENERATIONS):
    fitness_scores = evaluate_population(population, df)
    print("Generation", i+1, "- Best Fitness Score:", max(fitness_scores))
    population = evolve_population(population, fitness_scores, MUTATION_RATE)

# Encontrando o melhor indivíduo
fitness_scores = evaluate_population(population, df)
best_individual = population[np.argmax(fitness_scores)]
model_genes = best_individual[:LOOKBACK_PERIOD+1]
strategy_genes = best_individual[LOOKBACK_PERIOD+1:]

# Criando o modelo de previsão final
model = LinearRegression()
X = []
for i in range(LOOKBACK_PERIOD, 0, -1):
    X.append(df.iloc[-i]['Price'])
X.append(df.iloc[-1]['Price'])
X = np.array(X).reshape(-1, 1)
y = np.array(df['Price'][-(LOOKBACK_PERIOD+1):])
model.fit(X, y)

# Fazendo a previsão final
X = np.array(df['Price'][-LOOKBACK_PERIOD-1:]).reshape(-1, 1)
y = np.array(df['Price'][-LOOKBACK_PERIOD:])
prediction = model.predict(X)[-1]
if strategy_genes[0] > 0:
    prediction *= (1 + strategy_genes[0])
else:
    prediction *= (1 - strategy_genes[0])
if strategy_genes[1] > 0:
    prediction += strategy_genes[1]
else:
    prediction -= strategy_genes[1]

# Imprimindo a previsão final
print("Final Prediction:", prediction * 100)