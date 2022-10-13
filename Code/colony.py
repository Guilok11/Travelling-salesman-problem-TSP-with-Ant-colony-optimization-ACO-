from copy import deepcopy
import numpy as np
from numpy import append, inf
import random
import functions
import time

with open("C:/Users/guilo/Downloads/Teste/outro/grafos de entrada/Entrada 10.txt", "r") as txt_file:
    vertice = int(next(txt_file))
    distance_array = np.array([list(map(int, line.split())) for line in txt_file])

ant = 3
iterations = 20
initial_pheromone = 0.1
alpha = 1
beta = 1
pheromone_evaporation_rate = 0.01
Q = 10
#vertice = ?

overall_best_distance = +inf
overall_best_path = np.zeros((1, vertice+1))
pheromone = 0.1 * np.ones((vertice, vertice))
draw_first_position = np.random.randint(0, vertice)


#EXECUTA A EVAPORAÇÃO
#ATUALIZA A MATRIZ DE FEROMONIOS COM BASE NA CONTRIBUIÇÃO DE CADA FORMIGA
#VALOR É ARMAZENADO PARA A IDA E VOLTA


product_p_v = functions.product_pheromone_visibility(distance_array, pheromone)
visibility_sum = functions.calculate_visibility_sum(vertice, product_p_v)
probability = functions.calculate_probability(vertice, product_p_v, visibility_sum)

current_position = draw_first_position

sum = functions.calculate_probability_sum(vertice, current_position, probability)
 
#FAZ UMA COPIA DA PROBABILIDADE
copy_probability = deepcopy(probability)

#contadores
cont = 0
moviment_ant = 1
ant_number = 0
flag = 0

ant_path = functions.initialize_ant_path(ant, draw_first_position, vertice)

#COPIA A MATRIZ INICIAL DAS FORMIGAS PARA FIM DE VERIFICAR SE UMA FORFIMA FICA PRESA EM UM VERTICE
copy_ant_path = deepcopy(ant_path)

while(cont != iterations):
    
    #INICIA LOOP PARA A PRIMEIRA FORMIGA 
    while(ant_number != ant):
        
        #INICIA A PRIMEIRA TOMADA DE DECISÃO DA FORMIGA 
        while(moviment_ant != vertice): 
            
            #SORTEIA VALOR DE 0 ATÉ A SOMA TOTAL DOS VALORES DE PROBABILIDADE DISPONIVEL(100%) PARA O METODO DA ROLETA
            draw = random.uniform(0, sum)
                  
            #SE O VALOR DA SOMA DAS LINHAS DA PROBABILIDADE FOR IGUAL A 0
            #ENTAO NAO EXISTE MAIS CAMINHOS NÃO VISITADOS PARA A FORMIGA PASSAR
            if(sum == 0.0):
                o_cont = 1
                l_cont = 2
                
                #VERIFICA O VETOR DOS MOVIMENTOS DA FORMIGA PARA VERIFICAR SE FOI REPETIDO ALGUM VERTICE
                #PULANDO A POSIÇÃO INICIAL QUE IRA SER IGUAL A FINAL
                #SE FOI REPETIDO FLAG RECEBE 1
                while(o_cont != vertice):
                    
                    aux = ant_path[ant_number][i]
                    
                    while(l_cont != vertice):
                        
                        if(aux == ant_path[ant_number][l_cont]):
                            
                            flag = 1
                            break
                        else:
     
                            l_cont += 1 
                    o_cont +=1
                    
                if(flag == 1):
                    break   
                
            
            #INICIA OS CACULOS PARA A ROLETA
            accumulated = 0
            for j in range(vertice):
                
                prob = copy_probability[current_position][j] / sum
                
                accumulated += prob
                
                #SE O VALOR SORTEADO FOR MENOR OU IGUAL O ACUMULADO ENTAO O VALOR É ACEITO COMO O PROXIMO MOVIMENTO
                #DA FORMIGA E SAI DO LAÇO
                
                if(draw <= accumulated):
                    next_position = j
                    j = vertice
                    break
            
            #O MOVIMENTO ESCOLHIDO É INSERIDO NA MATRIZ DOS CAMINHOS DAS FORMIGAS
            ant_path[ant_number][moviment_ant] = next_position
            
            #ARMAZENA A POSIÇÃO ANTIGA
            previous_position = current_position
  
            #INICIA O LAÇO PARA ZERAR A LINHA E A COLONA DA PROBABILIDADE DO VERTICE JA VISITADO
            for i in range(vertice):
                for j in range(vertice):
                    if i == previous_position or j == previous_position:
                        copy_probability[i][j] = 0
                        
            current_position = next_position
            
            #CACULA A SOMA DAS PROBABILIDADES DA MATRIZ DAS PROBABILIDADES APOS UMA DECISÃO DE MOVIMENTO TOMADA
            sum = 0
            sum = functions.calculate_probability_sum(vertice, current_position, copy_probability)

            #PASSA PARA O PROXIMO MOVIMENTO/TOMADA DE DECISÃO
            moviment_ant += 1

        #APOS UMA FORMIGA PERCORRER O CAMINHO
        #O VETOR DAS PROBABILIDADES RETORNA AO VALOR INICIAL PARA A PROXIMA FORMIGA TOMAR AS DECISÕES
        copy_probability = deepcopy(probability)    
            
        #ARMAZENA O VALOR INCIAL QUE FOI SORTEADO NO COMEÇO PARA A POSIÇÃO ATUAL 
        #PARA QUE A PROXIMA FORMIGA COMEÇE DO PONTO INICIAL
        current_position = draw_first_position
         
        #FAZ AS SOMA  DAS PROBABILIDADES PARA A DICISÃO INICIAL DA PROXIMA FORMIGA
        sum = 0
        sum = functions.calculate_probability_sum(vertice, current_position, copy_probability)  
        moviment_ant = 1

        
        #SE HOUVE REPETIÇÃO DE VERTICES NO CAMINHO DA FORMIGA FLAG ESTARA COM O VALOR 1
        #LOGO IRA ENTRAR NO IF 
        #FLAG RECERA 0 E A FORMIGA QUE REPETIU O CAIMNHO REFAZ O CAMINHO
        #CASO NAO, A PROXIMA FORMIGA TEM SUA VEZ
        #E A MATRIZ DOS CAMINHOS É ARMAZENADA PARA CASO A PROXIMA FORMIGA REPITA ALGUM VERTICE 
        if(flag == 1):
            flag = 0
            ant_number = ant_number
            ant_path = copy_ant_path
        else:
            ant_number += 1
            copy_ant_path = deepcopy(ant_path)
        
    #calcula as distancias
    ant_distances = functions.calculate_distances(vertice, ant, ant_path, distance_array)
    
    #FUNÇÃO ARGMIN PEGA O MENOR VALOR DA MATRIZ DAS DISTANCIAS
    idx = ant_distances.argmin()

    #VALOR É ARMAZENADO COMO O MELHOR VALOR ATUAL
    current_overall_best_path_distance = ant_distances[idx][0]
    
    print("Cont {}".format(cont+1))
    print("\nMelhor atual:\n", ant_distances[idx][0])

    #OVERALL POSSUI VALOR +INFINITO 
    #SE A ATUAL MENOR DISTANCIA É MENOR QUE +INFNITO ENTAO A ATUAL MENOR DISTANCIA SE TORNA A MELHOR DISTANCIA
    #E O CAMINHO DA FORMIGA "IDX" É ARMAZENADO ARRAY MELHOR SOLUÇÃO
    if(current_overall_best_path_distance < overall_best_distance):
        
        overall_best_distance = current_overall_best_path_distance
        
        for i in range(vertice+1):

            overall_best_path[0][i] = ant_path[idx][i]
            
    
    
    #CALCULA CONTRIBUIÇÕES
    matrix_contribution = functions.calculate_contribution(ant, vertice, ant_distances, Q)
    
    #ATUALIZA OS FEROMONIOS
    pheromone = functions.update_pheromone(ant, vertice, ant_path, matrix_contribution, pheromone, pheromone_evaporation_rate)
    
    #CALCULA NOVAMENTE MAS AGORA COM A MATRIZ DE FEROMONIOS MODIFICADA
    product_p_v = functions.product_pheromone_visibility(distance_array, pheromone)    
    
    #ZERA A MATRIZ DA SOMA DAS VISIBILIDADES PARA CALCULAR A NOVA MATRIZ COM VALORES ATUALIZADOS
    visibility_sum = visibility_sum*0
    sum = 0
    visibility_sum = functions.calculate_visibility_sum(vertice, product_p_v)
    
    #ZERA A MATRIZ DA PROBABILIDADE PARA CALCULAR A NOVA MATRIZ COM VALORES ATUALIZADOS
    probability = probability*0
    probability = functions.calculate_probability(vertice, product_p_v, visibility_sum)
    
    #POSIÇÃO SORTEADA VOLTA A SER A POSIÇÃO ATUAL
    current_position = draw_first_position
    
    #EXECUTA NOVAMENTE O CALCULO DA SOMA DAS PROBABILIDADES
    sum = functions.calculate_probability_sum(vertice, current_position, probability)
    
    #COPIA O VALOR DA MATRIZ DE PROBABILIDADE
    copy_probability = deepcopy(probability)
    
    #REININCIA A MATRIZ DOS CAMINHAS DAS FORMIGAS
    ant_path = ant_path*0
    ant_path = functions.initialize_ant_path(ant, draw_first_position, vertice)
        
    #REININCIA AS FORMIGAS 
    ant_number = 0
    cont += 1
    


print("\nMelhor Caminho = {}\nDistancia total = {}".format(overall_best_path,overall_best_distance))


##print(pheromone)
##print(visibility)   
#print(ant_path)
##print(visibility_sum)
##print(product_p_v)