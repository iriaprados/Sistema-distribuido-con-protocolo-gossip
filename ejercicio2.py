# EJERCICIO 2 - RED CON PROTOCOLO GOSSIP 

# Importar librerías 
import time
import random
import threading

mutex = threading.Lock() # Mutex, para evitar condicones de carrera 
parar = False  # Variable global para detener la propagación una vez alcanzado el límite

# ESTRUCTURA DE LA RED  
network = {
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

# FUNCIÓN GOSSIP
def gossip(node, message, network, visited, max_visits, p_stop, start_node): 
    
    global parar 

    # El nodo es 1, quien incia la comunicación
    if node == start_node: 
        with mutex: 
            if parar: # Si se ha alcanzado el máximo de visitas 
                return # Se sale de la función 
            visited.add(node) # No se ha alcanzado el máximo de visitas, sigue comunicación 
        print(f'Nodo {node} ha recibido el mensaje, nodo que inicia comunicación.')
        
        # Seleccionar tres vecinos del nodo 1, de forma aleatoria, y se indican como nuevos nodos 
        neighbors = network[node]
        for neighbor in random.sample(neighbors, min(3, len(neighbors))):
            gossip(neighbor, message, network, visited, max_visits, p_stop, start_node)
    
    # El nodo no es el nodo que inicia la comunicación 
    else:
        while node not in visited: # Mientras el nodo no se halla visitado
            time.sleep(0.1) # Pausa de 0.1 seg. entre las comunicaciones 
            
            with mutex:
                if len(visited) >= max_visits and not parar: # Se ha alcanzado el número máximo de visitas 
                    print(f"Se ha alcanzado el número máximo de visitas ({max_visits}). Nodos visitados: {len(visited)}")
                    parar = True  # Se activa parar, para finalizar la ejecucción de "gossip"
                if parar:
                    return  # Salir si se ha alcanzado el máximo y se debe detener
            
            if random.random() > p_stop: # Si el número aleatorio es mayor al valor de la probabilidad de p_stop 
                with mutex:
                    visited.add(node) # Comunicar con el nodo 
                print(f'Nodo {node} ha recibido el mensaje.')
                
                # Seleccionar hasta tres vecinos, para continuar con la propagación
                neighbors = network[node]
                for neighbor in random.sample(neighbors, min(3, len(neighbors))):
                    gossip(neighbor, message, network, visited, max_visits, p_stop, start_node)

def main():
    global parar
    start_node = 1
    message = "Hello"
    visited = set()
    max_visits = 10
    p_stop = 0.4
    parar = False  
    
    threads = []
    for node in network.keys():
        thread = threading.Thread(target=gossip, args=(node, message, network, visited, max_visits, p_stop, start_node))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
