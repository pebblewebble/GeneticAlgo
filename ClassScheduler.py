from collections import namedtuple
import random
from typing import List
from random import choices

# For Genome, I am thinking of having a list containing a list of ints instead
Genome: List[List[str]] = [[] for _ in range(5)]
Class = namedtuple("Class", ["name", "duration", "value", "num_students"])
Day = namedtuple("Day", ["name", "available_duration"])
ClassesList = [
    Class("SPCC", "2", "5", "30"),
    Class("PSMOD", "2", "5", "30"),
]
DaysList = [Day("Monday", "5"), Day("Tuesday", "10")]


def generate_genome():
    copyOfClass = list(ClassesList.copy())
    schedule = []
    for x in range(len(DaysList)):
        todayClass = []
        for i, classs in enumerate(copyOfClass):
            # 50 percent chance to put class into current day
            if random.randint(0, 1) == 1:
                todayClass.append(list(classs))
                copyOfClass.remove(classs)
        schedule.append(todayClass)
    print(len(schedule))
    return schedule


def generate_population(size: int, genome_length: int):
    population = []
    for _ in range(size):
        population.append(generate_genome(genome_length))
    return population


# Thought process
# What would replace weight limit for classes?
# Instead of weight limit, it should be overlaps for classes?
# But having an overlap limit feels useless as you wouldn't want it to ever be larger than 0
# Value was still be included just in case in the future I want to have a more favored class
# Need to think of a way to handle sequences of the class
def fitness(genome: Genome, classes: List[Class], days: List[Day]) -> int:
    mapGenomeToClass = dict(zip(genome, classes))
    duration_taken = 0
    value = 0
    for x, currGenome in enumerate(days):
        for y, classs in enumerate(classes):
            duration_taken += int(classs[x].duration)

    # for x, day in enumrate(days):
    #     for i, classs in enumerate(classes):
    #         if genome[i] == 1:
    #             duration_taken += int(classs.duration)
    #             value += int(classs.value)
    #
    #             if duration_taken > available_duration:
    #                 return 0
    return value


x = 0
while x != 100:
    x = x + 1
    print(generate_genome())
    print("\n")
# fitness(generate_genome, ClassesList, DaysList)
