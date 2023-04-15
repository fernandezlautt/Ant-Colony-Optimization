import random
import numpy as np

EVAPORATION_RATE = 0.5
ALPHA:float = 1.0
BETA:float = 1.0

class Ant:
    
    location:int
    ant_path:np.ndarray=np.empty(0, dtype=int)
    acu_distance:int
    next_point:int

    
    def __init__(self,start_location:int) -> None:
        self.location = start_location
        self.ant_path=np.append(self.ant_path, start_location)
        self.acu_distance = 0
        pass
    
    def ant_move(self, distances:np.ndarray, pheromone:np.ndarray) -> None:
        
        options = np.arange(distances.size, dtype=int)
        probabilities = np.zeros(distances.size, dtype=float)
        distances_pondered:np.ndarray
        pheromone_pondered:np.ndarray
        epsilon = 1e-8 #To not divide by 0
    
        for i in range (self.ant_path.size):
            options[self.ant_path[i]] = 0
            distances[self.ant_path[i]] = 0
            pheromone[self.ant_path[i]] = 0
            pass

        distances_pondered = distances + epsilon
        pheromone_pondered = pheromone + epsilon
        distances_pondered = np.power(distances, -BETA)
        pheromone_pondered = np.power(pheromone, ALPHA)
        distances_pondered[np.isinf(distances_pondered)] = 0
        pheromone_pondered[np.isinf(pheromone_pondered)] = 0
    
        for i in range (probabilities.size):
            if(distances_pondered[i] < np.Infinity and pheromone_pondered[i] < np.Infinity):
                probabilities[i] = (pheromone_pondered[i]*distances_pondered[i])/(np.dot(pheromone_pondered,distances_pondered))
            pass
        
        next_point = np.random.choice(options, p=probabilities)
        
        #consecuences of the move
        self.ant_path=np.append(self.ant_path, next_point)
        self.location = next_point
        self.acu_distance = self.acu_distance + distances[next_point]
    
        pass
    pass


def aco(size_graph,amount_ants) -> np.ndarray:
    
    distances:np.ndarray
    ants:np.ndarray = np.empty(amount_ants, dtype=Ant)
    pheromone:np.ndarray = np.ones((size_graph,size_graph), dtype=int)
    cycles:int = 0
    t:int = 0
    
    #Create a random graph of distances
    distances = np.zeros((size_graph,size_graph), dtype=int)
    distances[np.triu_indices(size_graph, k=1)] = np.random.randint(low=10, high=1000,size=int((distances.size-size_graph)/2))
    distances = distances + distances.T
    for i in range (amount_ants):
        np.put(ants,i,Ant(random.randint(0,size_graph-1)))
        pass
    
    while(cycles < 2500):
        while(t<size_graph-1):
            for i in range (amount_ants):
                ants[i].ant_move(distances[ants[i].location], pheromone[ants[i].location])
                pass
            t = t + 1
            pass
        for i in range (amount_ants):
            
            pass
        cycles = cycles + 1
    print (distances)

aco(15,10)
