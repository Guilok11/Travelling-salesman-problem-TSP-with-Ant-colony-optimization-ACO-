import numpy as np
from numpy import inf
import random

def update_pheromone(ant, vertice, ant_path, matrix_contribution, pheromone, pheromone_evaporation_rate):
    
    pheromone = pheromone-pheromone_evaporation_rate
    
    for each_ant in range(ant):
        for each_vertex in range(vertice):
            
            m = ant_path[each_ant][each_vertex]
            m = int(m)
            
            n = ant_path[each_ant][each_vertex+1]
            n = int(n)
            
            pheromone[m][n] += matrix_contribution[each_ant][each_vertex]
            
            pheromone[n][m] += matrix_contribution[each_ant][each_vertex]
    
    return pheromone

#CALCULA A PRIMEIRA VISIBILIDADE
def product_pheromone_visibility(distance_array, pheromone):
    visibility = 1 / distance_array
    visibility[visibility == inf] = 0
    
    product_p_v = pheromone*visibility
    
    return product_p_v

#CALCULA A CONTRIBUIÇÃO DE CADA FORMIGA E ARMAZENA NA MATRIZ DE CONTRIBUIÇÃO
def calculate_contribution(ant, vertice, ant_distances, Q):
    matrix_contribution = np.zeros((ant, vertice))
    
    for each_ant in range(ant):
        for each_vertex in range(vertice): 
            matrix_contribution[each_ant][each_vertex] = Q / ant_distances[each_ant][0]
    
    return matrix_contribution

#CALCULA A DISTANCIA DE TODAS AS FORMIGAS E ARMAZENA EM UMA MATRIZ DE 1 COLUNA
#CADA LINHA DESSA MATRIZ REPRESENTA A DISTANCIA PERCORRIDA POR X FORMIGA
def calculate_distances(vertice, ant, ant_path, distance_array):
    ant_distances = np.zeros((ant, 1))
    total = 0
    
    for each_ant in range(ant):
        for i in range(vertice):

            m = ant_path[each_ant][i]
            m = int(m)

            n = ant_path[each_ant][i+1]
            n = int(n)
            total = distance_array[m][n] + total
        ant_distances[each_ant][0] = total
        total = 0
        
    return ant_distances

#CALCULA A SOMA DA VISIBILIDADE
def calculate_visibility_sum(vertice, product):
    sum = 0
    visibility_sum = np.zeros((vertice, 1))
    
    for i in range(vertice):
        for j in range(vertice):
            sum += product[i][j]
        visibility_sum[i][0] = sum
        sum = 0
    return visibility_sum

#CALCULA A PRIMEIRA PROBABILIDADE
def calculate_probability(vertice, product, visibility_sum):
    probability = np.zeros((vertice, vertice))
    
    for i in range(vertice):
        for j in range(vertice):
            probability[i][j] = product[i][j] / visibility_sum[i][0]

    return probability

#CALCULA A SOMA DAS PROBABILIDADES DA POSIÇÃO SORTEADA
def calculate_probability_sum(vertice, current_position, probability):
    sum = 0
    for j in range(vertice):
        sum += probability[current_position][j]
    
    return sum

#INICIA TODAS AS FORMIGAS NA POSIÇÃO SORTEADA E BOTA A POSIÇÃO SORTEADA NO FINAL
def initialize_ant_path(ant, draw_first_position, vertice):
    ant_path = np.zeros((ant, vertice+1))
    
    for i in range(ant):
        ant_path[i][0] = draw_first_position
        ant_path[i][vertice] = draw_first_position

    return ant_path