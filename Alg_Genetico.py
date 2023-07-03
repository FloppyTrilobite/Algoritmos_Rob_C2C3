#Algoritmo Genético
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
import math

#! Definir a representação de indivíduos (vetor binário) 

#[peso,valor]
itens = [[2,1],
        [4,2],
        [5,3],
        [2,2],
        [4,3],
        [6,2]]

#população
pool = [[],[],[],[],[],[],[],[],[],[]]

cpd_peso  = 11 #capacidade máxima (peso)
cpd_qtd = 4 #capacidade máxima (itens)
qtd_ger = 25 #quantidade de gerações
qtd_pool = 10 #número de indivíduos na população

qtd_itens = len(itens) #quantidade de itens

#! Criar população inicial aleatória

for i in range (qtd_pool):
    for j in range (qtd_itens):
        aux = random.randint(0, 1)
        pool[i].append(aux)
    #print(pool)
    #print("\n")


def assign_values(cod_gen, itens):
    soma_valor = 0
    soma_peso = 0
    for i in range(len(cod_gen)):
        if (cod_gen[i] == 1):
            soma_valor = soma_valor + itens[i][1]
            soma_peso = soma_peso + itens[i][0]

    aux = [soma_peso, soma_valor]
    return aux

#print(pool[0])
#print (assign_values(pool[0],itens))

def create_child(a,b):
        a = a[:len(a)//2]
        b = b[len(b)//2:]
        c = a+b
        return c

def mutate(a):
        #print("\n pre-mutate: ", a)
        b = random.sample(range(0, len(a)),math.ceil(len(a)/3))
        for k in range(len(b)):
            if (a[b[k]] == 0):
                a[b[k]] = 1
            else:
                a[b[k]] = 0
        #print("\n post-mutate: ", a)
        return a

#início (t=0)
result = [[],[]] 
for i in range (qtd_ger+1): #qtd_ger
    #! Avaliar a população (rankear)
    ger = []
    peso_ger = 0
    valor_ger = 0
    for j in range (qtd_pool): #para cada item da população
        peso = 0 
        valor = 0 
        qtd = 0 #quantidade de itens na mochila
        #critérios: qtd = ou < cpd_qtd (capacidade de itens na mochila), peso = ou < cpd_peso (capacidade de peso da mochila), valor
        for k in range (len(pool[j])):
            qtd = qtd + pool[j][k]
        #print(qtd)
        if (qtd <= cpd_qtd):
            aux = assign_values(pool[j],itens)
            peso = aux[0]
            valor = aux[1]
            
            if (peso <= cpd_peso):
                ger.append(aux)
                peso_ger = peso_ger + peso
                valor_ger = valor_ger + valor                       
            else:
                ger.append([0,0])
        else:
                ger.append([0,0])

    #print(pool)
    #print("\n", ger)

    for j in range(len(ger)):
        for k in range(len(ger)):
            if (ger[j] > ger[k]):
                aux = ger[k]
                ger[k] = ger[j]
                ger[j] = aux

                aux = pool[k]
                pool[k] = pool[j]
                pool[j] = aux

    #print(ger)    
    #print("\nvalor =", valor_ger/qtd_pool)
    #print("peso =", peso_ger/qtd_pool)
    #print("\n", pool)

    #! Selecionar e Cruzar
    for j in range (math.floor(qtd_pool/2)): #apagar a última metade
        pool.pop()

    #print("\n", pool)
    
    #escolher pais, genes metade-metade, dentre a primeira metade, e criar a segunda metade
    for j in range (len(pool)):
        pick = random.sample(range(0, len(pool)),2)
        #print(pick)
        a = pool[pick[0]]
        #print(a)
        b = pool[pick[1]] 
        #print(b)
        pool.append(create_child(a,b))

    #print("\n", pool)

    #! Mutações aleatórias
    #escolher aleatoriamente 1/3 dos itens e inverter para 20% da população (arrendondado para cima)
    for j in range (math.ceil(qtd_pool/5)):
        a = random.randint(0, len(pool)-1)
        #print(pool[a])
        pool[a] = mutate(pool[a])

    #fim da geração
    #print("\nvalor =", valor_ger/qtd_pool)
    #print("peso =", peso_ger/qtd_pool)
    result[0].append(peso_ger/qtd_pool)
    result[1].append(valor_ger/qtd_pool)

#resultados
print ("\n",result,"\n")

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

df = pd.DataFrame({
    'peso': result[0],
    'média(peso)': [np.mean(result[0]) for i in range(len(result[0]))],
    "máximo(peso)": 11,
    'valor': result[1],
    'média(valor)': [np.mean(result[1]) for i in range(len(result[1]))],
    'maior(valor)': np.max(result[1])
    })

df.plot()
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.show()