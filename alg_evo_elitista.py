import math
import random
import matplotlib.pyplot as plt
from numpy import mean, std

qtd_individuos = 100
qtd_pais = 15
qtd_filhos = 200
n_geracoes = 500
qtd_var_objetos = 30
xMax = 15
xMin = -15
tau = 1 / math.sqrt(qtd_individuos)
episilon = 0.0000000000000001
dp_max = 15

geracoes = []
melhores_geracoes = []
media_geracoes = []
dp_geracoes = []

#funcao Ackley
def funcAckley(lista_x):
    c1 = 20
    c2 = 0.2
    c3 = 2 * math.pi
    n = len(lista_x)

    somador = []
    for xi in lista_x:
        somador.append(math.pow(xi, 2))

    primeiro_somador = sum(somador)
    primeiro_parenteses = (-c2) * math.sqrt((1/n) * primeiro_somador)
    z = (-c1) * math.exp(primeiro_parenteses)

    somador2 = []
    for xi in lista_x:
        somador2.append(math.cos(c3 * xi))

    segundo_somador = sum(somador2)
    segundo_parenteses = math.exp((1/n) * segundo_somador)

    result = z - segundo_parenteses + c1 + math.exp(1)
    return result

#funcao fitness
def funcFitness(individuo):
    fitness = funcAckley(individuo[:qtd_var_objetos])
    return fitness

#funcao geradora de invididuo
def individuo():
    var_objetos = []
    for i in range(qtd_var_objetos):
        var_objetos.append(random.uniform(xMin, xMax))
    tam_passo_mutacao = random.uniform(episilon, dp_max)
    fitness = funcFitness(var_objetos)
    individuo = var_objetos + [tam_passo_mutacao] + [fitness]
    return individuo

#funcao geradora da populacao
def populacao():
    populacao = []
    for i in range(qtd_individuos):
        populacao.append(individuo())
    return populacao

#funcao selecao de pais
def selecao_pais(populacao):
    pais_selecionados = []

    for i in range(qtd_pais):
        pais_selecionados.append(random.choice(populacao))

    return pais_selecionados

#funcao de recombinacao
def recombinacao(pais_selecionados, qtd_pais_selecionados):
    var_objetos = []
    for i in range(qtd_var_objetos):
        var_objetos.append(random.choice(pais_selecionados)[i])
    tam_passo_mutacao = sum(pai[len(pai) - 2] for pai in pais_selecionados)/qtd_pais_selecionados
    filho = var_objetos + [tam_passo_mutacao] + [funcFitness(var_objetos)]
    return filho

#funcao de mutacao
def mutacao(filho):
    dis_lognormal = math.exp(tau * random.gauss(0, 1))
    tam_passo_mutacao = filho[len(filho) - 2]
    novo_tam_passo_mutacao = tam_passo_mutacao * dis_lognormal

    if novo_tam_passo_mutacao < episilon:
        novo_tam_passo_mutacao = episilon

    for i in range(qtd_var_objetos):
        nova_var_objeto = filho[i] + (novo_tam_passo_mutacao * random.gauss(0, 1))
        if xMin <= nova_var_objeto and nova_var_objeto <= xMax:
            filho[i] = nova_var_objeto
    return (filho, novo_tam_passo_mutacao)

#funcao de selecao de sobreviventes (μ + λ)
def selecao_sobreviventes(filhos_e_pais_selecionados):
    filhos_decrescente = sorted(filhos_e_pais_selecionados, key=lambda i: i[len(i) - 1])
    return filhos_decrescente[:qtd_individuos]

#geracao da populacao inicial
pop = populacao()
print(pop)

#melhor individuo
melhor_individuo = pop[0]
print(melhor_individuo)

#lista dos fitness de todos os individuos da populacao
lista_fitness = []
for individuo in pop:
    lista_fitness.append(individuo[len(individuo)-1])

geracoes.append(0)
melhores_geracoes.append(pop[0][qtd_var_objetos + 1])
media_geracoes.append(mean(lista_fitness))
dp_geracoes.append(std(lista_fitness))

for geracao in range(n_geracoes):
    #melhor fitness e numero da geracao
    print('Geração:', geracao, '- Melhor fitness:', melhor_individuo[qtd_var_objetos+1])

    #selecao, recombinacao e geracao dos filhos
    filhos = []
    for i in range(qtd_filhos):
        pais_selecionados = selecao_pais(pop)
        dois_pais = random.sample(pais_selecionados, 2)
        filhos.append(recombinacao(dois_pais, 2))

    #mutacao dos filhos
    for filho in filhos:
        res_mutacao = mutacao(filho)
        filho[len(filho) - 2] = res_mutacao[1]
        filho[len(filho) - 1] = funcFitness(res_mutacao[0])

    #selecao de sobreviventes
    #print('filhos:', filhos)
    pop = selecao_sobreviventes(filhos+pais_selecionados)

    #atualizacao do melhor individuo da populacao
    if melhor_individuo[qtd_var_objetos + 1] > pop[0][qtd_var_objetos+1]:
        melhor_individuo = pop[0]

    #parametros para a plotacao dos graficos
    lista_fitness = []
    for individuo in pop:
        lista_fitness.append(individuo[len(individuo) - 1])

    geracoes.append(geracao)
    melhores_geracoes.append(pop[0][qtd_var_objetos + 1])
    media_geracoes.append(mean(lista_fitness))
    dp_geracoes.append(std(lista_fitness))

    if melhor_individuo[qtd_var_objetos + 1] == 0:
        print("Geração de parada:", geracao)
        break

print()
print("Melhor fitness da população:", melhor_individuo[qtd_var_objetos+1])

fig1, ax1 = plt.subplots()
ax1.set_title('Resultados - Elitista')
ax1.plot(geracoes, melhores_geracoes, color='#17a589', label='Melhor')
ax1.plot(geracoes, media_geracoes, color='red', label='Média')
ax1.plot(geracoes, dp_geracoes, color='#f4d03f', label='Desvio Padrão')
plt.ylabel('Fitness')
plt.xlabel('Gerações')
plt.legend()
plt.show()

