import abc
import random
import numpy as np

EVAPORATION_RATE:float = 0.5
ALPHA:float = 1.0
BETA:float = 1.0
Q = 1000
AMOUNT_CYCLES:int = 500

#Elitist
ELITIST_AMOUNT:int = 3
ELITIST_CONSTANT:float =  8.0



class Ant:
    
    location:int
    ant_path:np.ndarray=np.empty(0, dtype=int)
    acu_distance:int
    next_point:int

    
    def __init__(self,start_location:int) -> None:
        self.location = start_location
        self.ant_path = np.array([start_location], dtype=int)
        self.acu_distance = 0
        pass
    
    def ant_move(self, distances:np.ndarray, pheromone:np.ndarray) -> None:
        
        options = np.arange(distances.size, dtype=int)
        probabilities = np.zeros(distances.size, dtype=float)
        probabilities_strategy:ProbabilitiesStrategy = ProbabilitiesStrategyNormal()
        if(self.ant_path.size != distances.size):
            for i in range (self.ant_path.size-1):
                distances[self.ant_path[i]] = 0
                pheromone[self.ant_path[i]] = 0
                pass
    
        if(self.ant_path.size == distances.size):
            next_point = self.ant_path[0]
            pass
        else:
            probabilities = probabilities_strategy.calculate_probabilities(distances, pheromone, self.ant_path)
            next_point = np.random.choice(options, p=probabilities)
            pass
        #consecuences of the move
        self.ant_path=np.append(self.ant_path, next_point)
        self.location = next_point
        self.acu_distance = self.acu_distance + distances[next_point]
    
        pass
    pass

class ProbabilitiesStrategy(abc.ABC):
    
    @abc.abstractmethod
    def calculate_probabilities(self, distances:np.ndarray, pheromone:np.ndarray, ant_path:np.ndarray) -> np.ndarray:
        pass
    pass

class ProbabilitiesStrategyNormal(ProbabilitiesStrategy):
    def calculate_probabilities(self, distances:np.ndarray, pheromone:np.ndarray, ant_path:np.ndarray) -> np.ndarray:
        probabilities:np.ndarray = np.zeros(distances.size, dtype=float)
        for i in range (probabilities.size):
            if(i in ant_path):
                probabilities[i] = 0
                pass
            else:
                probabilities[i] = pheromone[i]/pheromone.sum()
            pass
        pass
        return probabilities
    pass

class ProbabilitiesStrategyPondered(ProbabilitiesStrategy):
    def calculate_probabilities(self, distances:np.ndarray, pheromone:np.ndarray, ant_path:np.ndarray) -> np.ndarray:
        probabilities:np.ndarray = np.zeros(distances.size, dtype=float)
        epsilon = 1e-8 #To not divide by 0
        distances_pondered:np.ndarray
        pheromone_pondered:np.ndarray
        
        distances_pondered = distances + epsilon
        pheromone_pondered = pheromone + epsilon
        distances_pondered = np.power(distances, -BETA)
        pheromone_pondered = np.power(pheromone, ALPHA)
        distances_pondered[np.isinf(distances_pondered)] = 0
        pheromone_pondered[np.isinf(pheromone_pondered)] = 0
    
        for i in range (probabilities.size):
            if(distances_pondered[i] != 0 and pheromone_pondered[i] != 0):
                probabilities[i] = (pheromone_pondered[i]*distances_pondered[i])/(np.dot(pheromone_pondered,distances_pondered))
                pass
            pass
        pass
    pass

class PheromoneUpdateStrategy(abc.ABC):
    
    @abc.abstractmethod
    def update_pheromone(self, pheromone:np.ndarray, ants:np.ndarray) -> None:
        pass
    pass


class PheromoneUpdateStrategyElitist(PheromoneUpdateStrategy):
    def update_pheromone(self, pheromone:np.ndarray, ants:np.ndarray) -> np.ndarray:
        
        #find the best ELITIST_AMOUNT paths
        distances = np.array([[ant.acu_distance,ant] for ant in ants])
        
        #sort by distance
        distances = distances[distances[:,0].argsort()]

        #update pheromone
        for i in range (ELITIST_AMOUNT):
            for j in range (distances[i][1].ant_path.size-1):
                pheromone[distances[i][1].ant_path[j],distances[i][1].ant_path[j+1]] = pheromone[distances[i][1].ant_path[j],distances[i][1].ant_path[j+1]] + ELITIST_CONSTANT*(Q/distances[i][1].acu_distance)
                pheromone[distances[i][1].ant_path[j+1],distances[i][1].ant_path[j]] = pheromone[distances[i][1].ant_path[j],distances[i][1].ant_path[j+1]]
                pass
            pass
        return pheromone
    pass


def aco(size_graph,amount_ants) -> np.ndarray:
    
    distances:np.ndarray
    ants:np.ndarray = np.empty(amount_ants, dtype=Ant)
    pheromone:np.ndarray = np.ones((size_graph,size_graph), dtype=float)
    cycles:int = 0
    t:int = 0
    PHEROMONE_UPDATE_STRATEGY:PheromoneUpdateStrategy = PheromoneUpdateStrategyElitist()
    #ToDo
    #best_path:np.ndarray = np.empty(0, dtype=int)
    
    np.fill_diagonal(pheromone, 0)
    
    #Create a random graph of distances
    distances = np.zeros((size_graph,size_graph), dtype=int)
    distances[np.triu_indices(size_graph, k=1)] = np.random.randint(low=10, high=1000,size=int((distances.size-size_graph)/2))
    distances = distances + distances.T
    
    while(cycles < AMOUNT_CYCLES):
        t=0
        #initialize ants
        for i in range (amount_ants):
            np.put(ants,i,Ant(random.randint(0,size_graph-1)))
            pass
        
        while(t<size_graph):
            
            for i in range (amount_ants):
                distance_ant:np.ndarray = np.copy(distances[ants[i].location])
                pheromone_ant:np.ndarray = np.copy(pheromone[ants[i].location])
                ants[i].ant_move(distance_ant, pheromone_ant)
                pass
            t = t + 1
            
            pass
        pheromone = pheromone*EVAPORATION_RATE
        pheromone = PHEROMONE_UPDATE_STRATEGY.update_pheromone(pheromone, ants)
        cycles = cycles + 1
    
    for i in range (amount_ants):
        print("Ant: ", i)
        print("Path: ", ants[i].ant_path)
        print("Distance: ", ants[i].acu_distance)
        pass
    print(distances)

aco(10,10)
