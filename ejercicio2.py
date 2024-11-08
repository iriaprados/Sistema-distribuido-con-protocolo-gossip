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

    if node == start_node:  # Nodo inicial de comunicación
        with mutex: 
            if parar:  # Detener si se ha alcanzado el límite
                return
            visited.add(node)  # Agregar nodo a los visitados
        print(f'Nodo {node} ha recibido el mensaje, este es el nodo que inicia comunicación con el mensaje {message}')
        
        # Seleccionar tres vecinos al azar y continuar la propagación
        vecinos = network[node]
        for i in random.sample(vecinos, min(3, len(vecinos))):
            gossip(i, message, network, visited, max_visits, p_stop, start_node)
    
    else:  # Nodos que no son el nodo inicial
        while node not in visited:  # Mientras el nodo no se haya visitado
            time.sleep(0.1)  # Pausa entre comunicaciones
            
            with mutex:
                if len(visited) >= max_visits and not parar:  # Si el número de visitas es mayor o igual al número de nodos visitados 
                    # print(f"Se ha alcanzado el número máximo de visitas ({max_visits}). Nodos visitados: {len(visited)}")
                    parar = True # Parar poner a true 
                if parar:
                    return # Terminar la ejecucción 
                
            # Si el nodo no ha sido visitado 
            if node not in visited:
               
                with mutex:
                    visited.add(node)  # Se añade a la lista de los nodos visitados 
                print(f'Nodo {node} ha recibido el mensaje {message}.') # El nodo recibe el mensaje 
                
                if random.random() > p_stop: # Si la propabilidad generada aleatoriamenta (entre 0 y 1), es mayor a la probabilidad definida 
                    vecinos = network[node] # Para los nodos que se han definido en la red 
                    for i in random.sample(vecinos, min(3, len(vecinos))): # Se seleccionan hasta tres vecinos de forma aleatoria 
                        gossip(i, message, network, visited, max_visits, p_stop, start_node) 
                else:  # Decide no enviar el mensaje
                    print(f"Nodo {node} ha decidido no enviar el mensaje debido a la probabilidad.")
            return  # Salir después de procesar

# Función para main 
def main():
    global parar
    start_node = 1
    message = "Cotilleo!!"
    visited = set()
    max_visits = 10
    p_stop = 0.5
    parar = False  

    # Indicar nodos totales visitados 
    # start_time = time.time()
    # while time.time() - start_time < 1:  # Ejecutar durante 1 segundo
    #     time.sleep(0.1)  

    # Creación de los hilos 
    threads = [] # Lista para los hilos procesados 
    for node in network.keys(): # Para los nodos generados en la red 
        thread = threading.Thread(target=gossip, args=(node, message, network, visited, max_visits, p_stop, start_node)) # Los hilos ejecutan la función gossip, a la que se le indican sus argumentos
        threads.append(thread) # Añadir hilo a la lista
        thread.start() # Iniciar el hilo 
    
    for thread in threads: # Para los hilos de la lista 
        thread.join() # Esperar que terminen 
    
    print(f"\nSe ha alcanzado el número máximo de visitas ({max_visits}). Nodos visitados: {len(visited)}")

    print(f'\n{"★ "*58}')
    print(f'Han sido visitados {len(visited)} nodos, que han sido {visited}, del total de {len(network)} nodos que hay en la red.')
    print(f'{"★ "*58}\n')

if __name__ == "__main__":
    main()
