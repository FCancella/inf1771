from queue import PriorityQueue
import time
from TreeNode import TreeNode
import colorama

colorama.init()
print("\033[2J")   #apaga tela
print("\033[?25l") #apaga cursor

y = 0
x = 0

def read_file(filename):

    global x, y
    lines = None    
    start = (0,0)
    end = (0,0)

    with open(filename) as file:
        lines = file.readlines()

        j = 0
        for line in lines:
            lines[j] = line.strip('\n')
            
            if line.find('F') > -1:
                end = (line.find('F'), j)
            if line.find('I') > -1:
                start = (line.find('I'), j)
            j += 1

    x = len(lines[0])
    y = len(lines)

    return lines, start, end


def printMap(lines, actual):

    print()
    print()
    print()
            
    print("\033[%d;%dH" % (1, 1)) # y, x

    for j in range(y):
        for i in range(x):
            if actual[0] == i and actual[1] == j:
                print('█', end='')
            else:
                print(lines[j][i], end='')

        print()



def get_value(c):
    
    v = -1

    if c == '.' or c == 'I' or c == 'F':
        v = 1
    elif c == 'X':
        v = -1

    return v

def get_char_from_map(mapa, coord):
    return mapa[coord[1]][coord[0]]

def get_value_from_map(mapa, coord):
    return get_value(get_char_from_map(mapa, coord))


def add_valid_pos(nb, mapa, coord):        
    if get_value_from_map(mapa, coord) > -1:
        nb.append(coord)

def get_neighborhood(mapa, coord):
    
    nb = []
    if coord[0] == 0:
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
    
    elif coord[0] == x - 1:
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    

    if coord[1] == 0:
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
    
    elif coord[1] == y - 1:
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    return nb


mapa, start, end = read_file('mapa10.txt')


def busca_largura(mapa):
    c = 0
    visitados = []
    fila = [TreeNode(start, 0)]

    while fila != []:
        c+=1
        atual = fila.pop(0) # retira o primeiro elemento da fila
        dist_atual = atual.get_value_gx()
        coord_atual = atual.get_coord()
        visitados.append(coord_atual)
        #printMap(mapa, coord_atual)
        #time.sleep(0.1)

        if coord_atual == end:
            print(" > Encontrei solucao")
            print(" > Distancia total: ", dist_atual)
            print(" > Numero de nos expandidos: ", c)
            return atual

        for vizinho in get_neighborhood(mapa, coord_atual):
            if vizinho not in visitados:
                g_x = dist_atual + get_value_from_map(mapa, vizinho)
                filho = TreeNode(vizinho, g_x)
                filho.set_parent(atual)
                
                fila.append(filho)





def busca_profundidade(mapa):
    c = 0
    visitados = []
    pilha = [TreeNode(start, 0)]

    while pilha != []:
        c+=1
        atual = pilha.pop() # retira o ultimo elemento da pilha
        dist_atual = atual.get_value_gx()
        coord_atual = atual.get_coord()
        visitados.append(coord_atual)
        #printMap(mapa, coord_atual)
        #time.sleep(0.1)

        if coord_atual == end:
            print(" > Encontrei solucao")
            print(" > Distancia total: ", dist_atual)
            print(" > Numero de nos expandidos: ", c)
            return atual

        for vizinho in get_neighborhood(mapa, coord_atual):
            if vizinho not in visitados:
                g_x = dist_atual + get_value_from_map(mapa, vizinho)
                filho = TreeNode(vizinho, g_x)
                filho.set_parent(atual)
                
                pilha.append(filho)




def manhattan_distance(_from, to):
    # |x2 - x1| + |y2 - y1|
    return abs(to[0] - _from[0]) + abs(to[1] - _from[1])

def busca_a_estrela(mapa):

    num_iter = 0

    visitados = []

    fronteira = PriorityQueue()

    fronteira.put(TreeNode(start, manhattan_distance(start, end), 0))  #fronteira ← InsereNaFila(FazNó(EstadoInicial), fronteira)

    while fronteira:  #loop do while fronteira != vazio

        num_iter += 1

        

        no_arv = fronteira.get()

        

        distancia_atual = no_arv.get_value_gx()

        posicao_atual = no_arv.get_coord()  #   nó ← RemovePrimeiro(fronteira)

        visitados.append(posicao_atual)

    

        #printMap(mapa, posicao_atual)

        #time.sleep(0.1)

        if posicao_atual == end:    #   se nó[Estado] for igual a EstadoFinal então

            #printMap(mapa, posicao_atual)

            print(" > Encontrei solucao em", num_iter, "iteracoes e com distancia",distancia_atual)

            return no_arv

        #

        #   fronteira ← InsereNaFila(ExpandeFronteira(Mapa, nó), fronteira)
        for vizinho in get_neighborhood(mapa, posicao_atual):

                    if vizinho not in visitados:

                        h_x = manhattan_distance(vizinho, end)

                        g_x = distancia_atual + get_value_from_map(mapa, vizinho)

                        f_x = h_x + g_x

                        no_filho = TreeNode(vizinho, f_x, g_x)

                        no_filho.set_parent(no_arv)

                        fronteira.put(no_filho)







no_final = busca_largura(mapa)
busca_profundidade(mapa)
busca_a_estrela(mapa)

# while no_final.get_parent() != None:
#     printMap(mapa, no_final.get_coord())
#     # print(no_final.get_coord())
#     no_final = no_final.get_parent()
#     time.sleep(0.1)
