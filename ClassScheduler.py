from collections import namedtuple
from typing import List
from random import choices

# For Genome, I am thinking of having a list containing a list of ints instead
Genome: List[List[int]] = [[] for _ in range(5)]
Classes = namedtuple("Class", ["name", "duration", "value", "num_students"])
Days = namedtuple("Day", ["name", "available_duration"])


def generate_genome(length: int):
    return choices([0, +1], k=length)


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
def fitness(
    genome: Genome, classes: List[Classes], days: List[Days], weight_limit: int
) -> int:
    if len(genome) != len(classes):
        raise ValueError("Genome and Classes are supposed to be the same")

    duration_taken = 0
    value = 0

    for x, day in enumrate(days):
        for i, classs in enumerate(classes):
            if genome[i] == 1:
                duration_taken += int(classs.duration)
                value += int(classs.value)

                if duration_taken > available_duration:
                    return 0
    return value