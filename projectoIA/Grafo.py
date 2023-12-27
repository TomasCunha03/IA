# Classe grafo para representaçao de grafos,
import math
from queue import Queue

import networkx as nx  # biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import matplotlib.pyplot as plt  # idem

from Nodo import Node


# Constructor
# Methods for adding edges
# Methods for removing edges
# Methods for searching a graph
# BFS, DFS
# Other interesting methods


class Graph:

    def __init__(self):
        self.m_nodes = []
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        self.m_h = {}  # dicionario para armazenar as heuristicas para cada nodo -< pesquisa informada

    def parse_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                data = line.strip().split(';')
                node1, coord1 = data[0], eval(data[1])
                node2, coord2 = data[2], eval(data[3])
                weight = int(data[4])
                self.add_edge(node1, coord1, node2, coord2, weight)

    #############
    #    escrever o grafo como string
    #############
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out += f"Node {key} ({self.get_node_by_name(key).getCoord()}): {str(self.m_graph[key])}\n"
        return out

    ################################
    #   encontrar nodo pelo nome
    ################################

    def get_node_by_name(self, name):
        for node in self.m_nodes:
            if node.getName() == name:
                return node
        return None

    ############################
    #   imprimir arestas
    ############################

    def imprime_aresta(self):
        listaA = ""
        for nodo, arestas in self.m_graph.items():
            for (nodo2, custo) in arestas:
                coord1 = self.get_node_by_name(nodo).getCoord()
                coord2 = self.get_node_by_name(nodo2).getCoord()
                listaA += f"{nodo} ({coord1}) -> {nodo2} ({coord2}) custo: {str(custo)}\n"
        return listaA

    ################
    #   adicionar   aresta no grafo
    ######################

    def add_edge(self, node1, coord1, node2, coord2, weight):
        n1 = Node(node1, coord1)
        n2 = Node(node2, coord2)
        if n1 not in self.m_nodes:
            n1_id = len(self.m_nodes)  # numeração sequencial
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if n2 not in self.m_nodes:
            n2_id = len(self.m_nodes)  # numeração sequencial
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))  # poderia ser n1 para trabalhar com nodos no grafo
        self.m_graph[node2].append((node1, weight))

    #############################
    # devolver nodos
    ##########################

    def getNodes(self):
        return self.m_nodes

    #######################################
    #    devolver o custo de uma aresta   #
    #######################################

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    ##############################
    #  dado um caminho calcula o seu custo
    ###############################

    def calcula_custo(self, caminho):
        # caminho é uma lista de nodos
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    ################################################################################
    #     procura DFS
    ####################################################################################

    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    #####################################################
    # Procura BFS
    ######################################################

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        else:
            return None
        return (path, custo)

    ###########################
    # desenha grafo  modo grafico
    #########################

    def desenha(self):
        lista_v = self.m_nodes
        g = nx.Graph()

        node_positions = {}
        node_labels = {}

        for nodo in lista_v:
            n = nodo.getName()
            coord = nodo.getCoord()
            g.add_node(n, pos=coord)
            node_positions[n] = coord
            node_labels[n] = f"{n}\nCoord: {coord}\nHeuristic: {self.m_h.get(n, 'N/A')}"

            for (adjacente, peso) in self.m_graph[n]:
                n2 = self.get_node_by_name(adjacente)
                coord2 = n2.getCoord()
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.get_node_attributes(g, 'pos')
        nx.draw_networkx(g, pos, with_labels=False, font_weight='bold', node_size=700, node_color='skyblue')

        edge_labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

        nx.draw_networkx_labels(g, node_positions, labels=node_labels)

        plt.draw()
        plt.show()


    ####################################33
    #    add_heuristica   -> define heuristica para cada nodo 
    ################################

    def add_heuristica(self, n, coord, estima):
        n1 = Node(n, coord)
        if n1 in self.m_nodes:
            self.m_h[n] = estima

    ## Utilizamos a distância euclideana para calcular a heuristica através da latitude e longitude
    def calcula_heuristica(self, n, objetivo):
        nAtual = self.get_node_by_name(n)
        nObj = self.get_node_by_name(objetivo)
        coordAtual = nAtual.getCoord()
        coordObj = nObj.getCoord()

        heuristica = int(round(math.sqrt((coordObj[1] - coordAtual[1]) ** 2 + (coordObj[0] - coordAtual[0]) ** 2)))

        return heuristica

    def calculate_all_heuristics(self, start_node_name, end_node_name):
        start_node = self.get_node_by_name(start_node_name)
        end_node = self.get_node_by_name(end_node_name)

        if start_node is None or end_node is None:
            print("Error: Invalid start or end node names.")
            return

        for node in self.m_nodes:
            heuristic_value = self.calcula_heuristica(node.getName(), end_node_name)
            self.add_heuristica(node.getName(), node.getCoord(), heuristic_value)
    def getH(self, nodo):
        return self.m_h[nodo]

    ##########################################
    #    A*
    ##########################################

    def getNeighbours(self, node):
        if node in self.m_graph:
            return self.m_graph[node]  # Placeholder - replace with actual logic
        else:
            return []

    def calcula_est(self, calc_heurist):
        min_estima = float('inf')
        min_node = None
        for node, est in calc_heurist.items():
            if est < min_estima:
                min_estima = est
                min_node = node
        return min_node

    def procura_aStar(self, start, end):
        open_list = {start}
        closed_list = set([])

        g = {}
        g[start] = 0

        parents = {}
        parents[start] = start
        n = None

        while len(open_list) > 0:
            calc_heurist = {}
            for v in open_list:
                calc_heurist[v] = g[v] + self.getH(v)

           # print("Current node:", n)
            #print("Open list:", open_list)
            #print("Closed list:", closed_list)
            #print("g values:", g)
            #print("Heuristic values:", calc_heurist)

            min_estima = self.calcula_est(calc_heurist)
            n = min_estima

            if n is None:
                print('Path does not exist!')
                return None

            if n == end:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                print('Optimal Path found:', reconst_path)
                print('Total Cost:', self.calcula_custo(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    '''def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        # n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                ##if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....

                print("\n")
                print(self.getH(v), "HEURISTICA")
                print(g[v], "NAO SEI")
                print(v, "NODO")
                if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....
                    print(g[v]+self.getH(v), "SOMA HEURISTICA")
                    n = v
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None'''

    def find_best_paths_for_final_nodes(self, initial_node, final_nodes):
        best_paths = {}  # Dictionary to store the best paths for each final node

        for final_node in final_nodes:
            path, cost = self.procura_aStar(initial_node, final_node)  # Run A* for each final node
            if path:
                best_paths[final_node] = (path, cost)  # Store the best path and its cost

        return best_paths
    ##########################################
    #   Greedy
    ##########################################

    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontra nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))
            # para todos os vizinhos  do nodo corrente

            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
