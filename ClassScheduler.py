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
def fitness(genome: Genome, classes: List[Class]) -> int:
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
    genomeWithFitness = [(currentGenome,fitness(currentGenome,ClassesList)) for currentGenome in population]
    #After giving them their fitness, we can now order them and then only take the top 2
    sortedByFitness = sorted(genomeWithFitness,key=lambda x:x[1],reverse=True)
    return [genome for genome,_ in sortedByFitness[:2]]

def single_point_crossover(firstGenome:Genome, secondGenome:Genome) -> Tuple[Genome, Genome]: 
    for day in firstGenome:
        if len(firstGenome[day])<2:    
            return firstGenome,secondGenome
        #p helps us determine the single point that we crossover
        p = randint(1, len(firstGenome[day]) - 1)
        # Basically puts a point in the genome to do the crossover, Genome A [0,1,1,0] Genome B [1,0,0,1] p=1,
        # the return [0,1,0,1],[1,0,1,0]
        firstGenome[day]= firstGenome[day][0:p] + secondGenome[day][p:]
        secondGenome[day]= secondGenome[day][0:p] + firstGenome[day][p:]
    return firstGenome,secondGenome
    
# Randomly mutate one of the bits in the genome
def mutation(genome: Genome) -> Genome:
    #Create a list to hold if the class has been conducted already or not
    class_assigned=[0]*len(ClassesList)
    for day in genome:
        for index in range(len(ClassesList)):
            #If the class has been conducted, become 1, else keep old value
            class_assigned[index]= 1 if genome[day][index]== 1 else class_assigned[index]

    for day in genome:
        #Gets the range of the genome
        index = randrange(len(genome[day]))
        if genome[day][index] == 0 and class_assigned[index] == 0:
            genome[day][index] = 1
            class_assigned[index] = 1
        elif genome[day][index] == 1:
            genome[day][index] = 0
            class_assigned[index] = 0
    return genome

def run_evolution(populationSize: int, fitness_limit: int,generation_limit: int) -> Tuple[Population, int]:
    population = generate_population(populationSize)
    for i in range(generation_limit):
        population = sorted(
            population, key=lambda genome: fitness(genome, ClassesList), reverse=True
        )


        best_fitness = fitness(population[0], ClassesList)
        print(f"Generation {i}, Best fitness: {best_fitness}") 


        # If the fitness of the best genome is larger than the fitness limit,
        # stop the process as it has reached the desired fitness limit
        if fitness(population[0], ClassesList) >= fitness_limit:
            break

        # Select the most fit genomes
        next_generation = population[0:2]
        for _ in range(int(len(population) / 2) - 1):
            parents = selection_pair(population)
            # Perform the crossover
            offspring_a, offspring_b = single_point_crossover(parents[0], parents[1])
            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)
            next_generation += [offspring_a, offspring_b]
        population = next_generation
    
    return population, i


def genome_to_classes(genome:Genome, classes:List[Class]) ->Dict[Day,List[Class]]:
    result = defaultdict(list)
    for day in genome: 
        for index in range(len(classes)):
            if genome[day][index]==1:
                result[day].append(classes[index].name)
    return result

# The maximum fitness that can be achieved is 38 in the classes list.
population, generations=run_evolution(5,35,10000)
print(f"number of generations:{generations}")
print(f"best solution:{genome_to_classes(population[0],ClassesList)}")

#After changing the mutation, it is harder to meet the desired fitness value which is 35



