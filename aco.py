import random
import numpy as np

REDUCTION_RATE = 0.2

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
        #ToDo
        options = np.arange(distances.size, dtype=int)
        probabilities = np.zeros(distances.size, dtype=float)
                
        for i in range (self.ant_path.size):
            options[self.ant_path[i]] = 0
            pheromone[self.ant_path[i]] = 0
            pass

        for i in range (probabilities.size):
            probabilities[i] = pheromone[i] * 1/(pheromone.sum())
            pass

        next_point = np.random.choice(options, p=probabilities)
        
        #consecuences of the move
        self.ant_path=np.append(self.ant_path, next_point)
        self.location = next_point
        self.acu_distance = self.acu_distance + distances[next_point]
        
        pass
    def pheromone_update() -> int:
        #ToDo
        
        pass
    
    pass


def aco(size_graph,amount_ants) -> np.ndarray:
    
    distances:np.ndarray
    ants:np.ndarray = np.empty(amount_ants, dtype=Ant)
    pheromone:np.ndarray = np.ones((size_graph,size_graph), dtype=int)
    
    #Create a random graph of distances
    distances = np.zeros((size_graph,size_graph), dtype=int)
    distances[np.triu_indices(size_graph, k=1)] = np.random.randint(low=10, high=1000,size=int((distances.size-size_graph)/2))
    distances = distances + distances.T
    for i in range (amount_ants):
        np.put(ants,i,Ant(random.randint(0,size_graph-1)))
        print("Hi I'm ant number: " + str(i) + " and my location is: " + str(ants[i].location))
        pass
    while():

        for i in range (amount_ants):
            ants[i].ant_move(distances[ants[i].location], pheromone[ants[i].location])
            pass
        for i in range (amount_ants):
            ants[i].pheromone_update()
    print (distances)

    
    
aco(15,10)
