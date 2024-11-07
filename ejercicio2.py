# EJERCICIO 2 - SISTEMA DISTRIBUIDO CON GOSSIP 

# IMPORTAR LIBRERÍAS 
import time  # Librería para las interrupciones. 
import random  # Librería para generar números aleatorios. 
import threading  # Librería para la implementación de hilos

mutex = threading.Lock()  # Crear mutex 

# ESTRUCTURA DE LA RED
network = {  # Diccionario para representar la red. 
    1: [2, 3, 4], 
    2: [1, 5, 6], 
    3: [1, 7, 8], 
    4: [1, 9, 10], 
    5: [2, 11, 12], 
    6: [2, 13], 
    7: [3, 14], 
    8: [3, 15], 
    9: [4], 
    10: [4], 
    11: [5], 
    12: [5], 
    13: [6], 
    14: [7], 
    15: [8] 
}

def gossip (node, message, network, visited, max_visits, p_stop, start_node): 
    
    if node == start_node:
        print(f"{node} inicia la propagación del mensaje: '{message}'")
        visited[node] = visited.get(node, 0) + 1
    else: 
        while node not in visited: 
            time.sleep(0.1)
    
    while visited [node] <= max_visits: 
        if random.random() <= p_stop:
            print(f'El nodo {node} decidió parar la propagación')
            break
        for vecino in network[node]: 
            if vecino not in visited: 
                print(f"{node} envía mensaje a {vecino}")
                visited[vecino] = visited.get(vecino, 0) + 1
        
        visited[node] += 1

        time.sleep(0.1)
    
    print(f"{node} ha alcanzado el límite de visitas o detenido la propagación.")

def main (): 
    start_node = 1       # Nodo de inicio
    message = "Hello"    # Mensaje a propagar
    visited = {}         # Conjunto de nodos visitados
    max_visits = 30       # Número máximo de visitas
    p_stop = 0.2         # Probabilidad de detener la propagación

    threads = []
    
    # Crear y lanzar hilos para cada nodo
    for node in network.keys():
        thread = threading.Thread(target=gossip, args=(node, message, network, visited, max_visits, p_stop, start_node))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

# Llamada a la función principal
main()