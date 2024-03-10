##Following a YouTube tutorial first to get a better grasp before applying it to my own use case
from collections import namedtuple
from typing import List, Callable, Tuple, Optional
from random import choices, randint, randrange, random
from functools import partial, wraps


# This genome will represent a bunch of 0s and 1s, so if it is [0,1,0] for items [Phone,Book,Bed], that means only book is present
Genome = List[int]
Population = List[Genome]
Thing = namedtuple("Thing", ["name", "value", "weight"])
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]

things = [
    Thing("Laptop", "15", "5"),
    Thing("Book", "5", "2"),
    Thing("Bottle", "10", "1"),
    Thing("Mouse", "5", "1"),
    Thing("Sejarah", "30", "10"),
    Thing("Bag", "50", "10"),
]


# Although Python can support dynamically typed variables, it is best to specify for future cases.
def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


# Modified code to my own liking/understanding as I see one liners a bit harder to read
def generate_population(size: int, genome_length: int) -> Population:
    population = []
    for _ in range(size):
        population.append(generate_genome(genome_length))
    return population


def fitness(genome: Genome, things: List[Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("Genome and Things are supposed to be the same")
    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += int(thing.weight)
            value += int(thing.value)

            if weight > weight_limit:
                return 0
    return value


# Selects two parents of two new generations
def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population, weights=[fitness_func(gene) for gene in population], k=2
    )


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a n b must be the same length")
    length = len(a)
    if length < 2:
        return a, b
    p = randint(1, length - 1)
    # Basically puts a point in the genome to do the crossover, Genome A [0,1,1,0] Genome B [1,0,0,1] p=1,
    # the return [0,1,0,1],[1,0,1,0]
    return a[0:p] + b[p:], b[0:p] + a[p:]


# Randomly mutate one of the bits in the genome
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = (
            genome[index] if random() > probability else abs(genome[index] - 1)
        )
    return genome


def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100,
    printer: Optional[PrinterFunc] = None,
) -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(
            population, key=lambda genome: fitness_func(genome), reverse=True
        )

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, i


def genome_to_things(genome: Genome, things: [Thing]) -> [Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]
    return result


population, generations = run_evolution(
    populate_func=partial(generate_population, size=10, genome_length=len(things)),
    fitness_func=partial(fitness, things=things, weight_limit=20),
    fitness_limit=740,
    generation_limit=100,
)
print(f"number of generations:{generations}")
print(f"best solution:{genome_to_things(population[0],things)}")
