import numpy as np

REDUCTION_RATE = 0.2

class Ant:
    
    location:tuple
    
    def __init__(self,start_location:tuple) -> None:
        self.location = start_location
        pass
    
    def pheromone_update() -> int:
        #ToDo
        pass
    
    def ant_move():
        #ToDo
        pass
    
    pass


def aco(size_graph,amount_ants) -> np.ndarray:
    
    distances:np.ndarray
    ants:np.ndarray
    
    distances = np.zeros((size_graph,size_graph), dtype=int)
    # generate random values for the elements outside the diagonal
    distances[np.triu_indices(size_graph, k=1)] = np.random.randint(low=10, high=100,size=int((size_graph*size_graph-size_graph)/2))
    
    #makes symmetric
    distances = distances + distances.T
    
    pheromone = np.zeros((size_graph,size_graph), dtype=int)

    for i in range (amount_ants):
        np.put(ants,i,Ant(()))
        
        pass    
        
    
    
    
aco(15,10)
