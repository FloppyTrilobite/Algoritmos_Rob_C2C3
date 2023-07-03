#Algoritmo baseado em Simulated Annealing (Recozimento Simulado)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
import math

#! Definindo o vetor de itens possíveis (vetor binário, igual o do algoritmo genético) 

#[peso,valor]
itens = [[2,1],
        [4,2],
        [5,3],
        [2,2],
        [4,3],
        [6,2]]

ind = []
viz = [] #

controle = 0
c = 1

cpd_peso  = 11 #capacidade máxima (peso)
cpd_qtd = 4 #capacidade máxima (itens)
qtd_ger = 50 #quantidade de gerações

qtd_itens = len(itens) #quantidade de itens

#! Criar um indivíduo inicial aleatório
for j in range (qtd_itens):
    aux = random.randint(0, 1)
    ind.append(aux)
    
#print(ind)
#print("\n")

def assign_values(cod_gen, itens):
    soma_valor = 0
    soma_peso = 0
    for i in range(len(cod_gen)):
        if (cod_gen[i] == 1):
            soma_valor = soma_valor + itens[i][1]
            soma_peso = soma_peso + itens[i][0]

    return soma_peso, soma_valor

def mutateX(a,c):
    #print("\n pre-mutate: ", a)
    b = random.sample(range(0, len(a)),c)
    for k in range(len(b)):
        if (a[b[k]] == 0):
            a[b[k]] = 1
        else:
            a[b[k]] = 0
    #print("\n post-mutate: ", a)
    return a


#início (t=0)
result = [[],[]] 
for i in range (qtd_ger): #qtd_ger
    peso_ind = 0 
    valor_ind = 0 
    qtd_ind = 0 #quantidade de itens na mochila

    peso_viz = 0 
    valor_viz = 0 
    qtd_viz = 0 #quantidade de itens na mochila

    #!cria um "vizinho" (com 1 gene de diferença)
    #caso uma solução melhor não esteja possível, tentar com mais variação
    if (controle == math.ceil(qtd_ger/5)):
        c = 2
    elif (controle == 0):
        c = 1

    viz = mutateX(ind.copy(),c)

    print(ind)
    print(viz)

    #quantidade
    for k in range (len(ind)):
        #print("\n ", ind[k],",",viz[k])
        qtd_ind = qtd_ind + ind[k]
        qtd_viz = qtd_viz + viz[k]
        #print("\n ", qtd_ind,",",qtd_viz)

    #valores
    peso_viz,valor_viz = assign_values(viz,itens)
    peso_ind,valor_ind = assign_values(ind,itens)
    
    print(" [",peso_ind,"],[",valor_ind, "]")
    print(" [",peso_viz,"],[",valor_viz, "]\n")

    aux = ind.copy()

    #!compara o vizinho com o indivíduo
    #critérios: itens, peso, valor
    if (qtd_ind <= cpd_qtd and qtd_viz <= cpd_qtd): #se a quantidade for menor ou igual ao máximo
        if (peso_ind <= cpd_peso and peso_viz <= cpd_peso): #se o peso for menor ou igual ao máximo
            if (valor_viz > valor_ind): #troca se o valor for maior que o atual
                ind = viz
        elif (peso_viz < peso_ind): #troca se for maior que máximo, menor que o atual 
            ind = viz                
    elif (qtd_viz < qtd_ind): #troca se for maior que o máximo, menor que o atual
        ind = viz
    
    if (aux == ind):
        controle = controle + 1
    else:
        controle = 0

    #fim da geração
    #print("\nvalor =", valor_ger/qtd_pool)
    #print("peso =", peso_ger/qtd_pool)
    print("controle =", controle, "\n")
    peso_ind,valor_ind = assign_values(ind,itens)
    result[0].append(peso_ind)
    result[1].append(valor_ind)

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

