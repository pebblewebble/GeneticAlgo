from collections import namedtuple, defaultdict
import random
from typing import List, Dict, Tuple
from random import choices,randint,randrange

# For Genome, I am thinking of having a list containing a list of ints instead
# Genome: List[List[str]] = [[] for _ in range(5)]
Class = namedtuple("Class", ["name", "duration", "value", "num_students"])
Day = namedtuple("Day", ["name", "available_duration"])
Genome = Dict[Day, List[int]]
Population = List[Genome]
ClassesList = [
    Class("SPCC", "2", "5", "30"),
    Class("PSMOD", "2", "5", "30"),
    Class("WPCS", "1", "2", "20"),
    Class("Java", "3", "10", "30"),
    Class("ABC", "1", "1", "50"),
    Class("SPCCT", "1", "5", "30"),
]
DaysList = [Day("Monday", "5"), Day("Tuesday", "10")]


def generate_genome() -> Genome :
    genome: Genome = defaultdict(list)
    currentAvailableClass = [1 for _ in range(len(ClassesList))]
    for day in DaysList:
        for i in range(len(currentAvailableClass)):
            if currentAvailableClass[i]==1:
                if random.randint(0, 1) == 1:
                    genome[day].append(1)
                    #Since the class has been added into another day, you can remove it from being 
                    #selected again
                    currentAvailableClass[i]=0
                else:
                    genome[day].append(0)
            else:
                genome[day].append(0)

    return genome

def generate_population(size: int) -> List[Genome]:
    population = []
    for _ in range(size):
        population.append(generate_genome())
    return population

# Thought process
# What would replace weight limit for classes?
# Instead of weight limit, it should be overlaps for classes?
# But having an overlap limit feels useless as you wouldn't want it to ever be larger than 0
# Value was still be included just in case in the future I want to have a more favored class
# Need to think of a way to handle sequences of the class
def fitness(genome: Genome, classes: List[Class], days: List[Day]) -> int:
    duration_taken = 0  
    fitnessValue = 0
    for day in genome:
        for index in range(len(classes)):
             if genome[day][index]==1:
                duration_taken += int(classes[index].duration)
                fitnessValue += int(classes[index].value)

             if duration_taken>int(day.available_duration):
                return 0
    return fitnessValue

#After calculating their fitness, we can now select the strongest parents
def selection_pair(population:Population) -> Population :
    genomeWithFitness = [(currentGenome,fitness(currentGenome,ClassesList,DaysList)) for currentGenome in population]
    #After giving them their fitness, we can now order them and then only take the top 2
    sortedByFitness = sorted(genomeWithFitness,key=lambda x:x[1],reverse=True)
    return [genome for genome,_ in sortedByFitness[:2]]

def single_point_crossover(firstGenome:Genome, secondGenome:Genome): 
    for day in firstGenome:
        if len(firstGenome[day])<2:    
            return firstGenome,secondGenome
        #p helps us determine the single point that we crossover
        p = randint(1, len(firstGenome[day]) - 1)
        # Basically puts a point in the genome to do the crossover, Genome A [0,1,1,0] Genome B [1,0,0,1] p=1,
        # the return [0,1,0,1],[1,0,1,0]
        print(firstGenome[day][0:p] + secondGenome[day][p:], secondGenome[day][0:p] + firstGenome[day][p:])
    
# Randomly mutate one of the bits in the genome
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for day in genome:
        #Gets the range of the genome
        index = randrange(len(genome[day]))
        genome[day][index] = 1 if genome[day][index]==0 else 0 
    return genome




population = generate_population(5)
# # for currentGenome in population:
print(selection_pair(population)[0],selection_pair(population)[1])
single_point_crossover(selection_pair(population)[0],selection_pair(population)[1])
    
