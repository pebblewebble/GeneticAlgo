from collections import namedtuple, defaultdict
import random
from typing import List, Dict
from random import choices

# For Genome, I am thinking of having a list containing a list of ints instead
# Genome: List[List[str]] = [[] for _ in range(5)]
Class = namedtuple("Class", ["name", "duration", "value", "num_students"])
Day = namedtuple("Day", ["name", "available_duration"])
Genome = Dict[Day, List[Class]]
ClassesList = [
    Class("SPCC", "2", "5", "30"),
    Class("PSMOD", "2", "5", "30"),
    Class("WPCS", "1", "2", "20"),
    Class("Java", "3", "10", "30"),
    Class("ABC", "1", "1", "50"),
    Class("SPCCT", "1", "5", "30"),
]
DaysList = [Day("Monday", "5"), Day("Tuesday", "10")]


def generate_genome() -> Genome:
    genome: Genome = defaultdict(list)
    copyList = ClassesList.copy()
    for day in DaysList:
        for cls in copyList:
            if random.randint(0, 1) == 1:
                genome[day].append(cls)
                copyList.remove(cls)
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
    value = 0
    for day in genome:
        classsesInDay = genome[day]
        for index in range(len(classsesInDay)):
            duration_taken += int(classsesInDay[index].duration)
            value += int(classsesInDay[index].value)

            if duration_taken>int(day.available_duration):
                return 0
    print(value)
    return value


fitness(generate_genome(), ClassesList, DaysList)
