from collections import namedtuple
from typing import List, Callable, Tuple, Optional, Dict
from random import choices, randint, randrange, random
from functools import partial

Class = namedtuple("Class", ["name", "duration", "value", "num_students"])
Day = namedtuple("Day", ["name", "available_duration"])
Genome = List[int]  # Changed from Dict to List
Population = List[Genome]

FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]

ClassesList = [
    Class("Physics", 3, 12, 25),
    Class("Literature", 2, 7, 30),
    Class("Computer Science", 4, 15, 20),
    Class("Chemistry", 3, 10, 22),
    Class("Economics", 2, 8, 28),
    Class("Music", 1, 5, 15),
    Class("Physical Education", 2, 6, 35)
]

DaysList = [Day("Monday", 6), Day("Tuesday", 4), Day("Wednesday", 5)]

def generate_genome() -> Genome:
    return [randrange(len(DaysList) + 1) for _ in range(len(ClassesList))]

def generate_population(size: int) -> Population:
    return [generate_genome() for _ in range(size)]

def fitness(genome: Genome, classes: List[Class], days: List[Day]) -> int:
    schedule = [[] for _ in range(len(days))]
    for class_index, day_index in enumerate(genome):
        if day_index < len(days):  # class is scheduled
            schedule[day_index].append(classes[class_index])

    total_value = 0
    for day_index, day_classes in enumerate(schedule):
        day_duration = sum(class_.duration for class_ in day_classes)
        if day_duration <= days[day_index].available_duration:
            total_value += sum(class_.value for class_ in day_classes)
        else:
            return 0  # Invalid schedule, exceeded day duration

    return total_value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) < 2:
        return a, b

    p = randint(1, len(a) - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = randrange(len(DaysList) + 1) if random() < probability else genome[index]
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
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for _ in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, i

def genome_to_schedule(genome: Genome, classes: List[Class], days: List[Day]) -> Dict[str, List[str]]:
    schedule = {day.name: [] for day in days}
    for class_index, day_index in enumerate(genome):
        if day_index < len(days):
            schedule[days[day_index].name].append(classes[class_index].name)
    return schedule

def print_schedule(genome: Genome, classes: List[Class], days: List[Day]):
    schedule = genome_to_schedule(genome, classes, days)
    for day_name, classes_scheduled in schedule.items():
        print(f"{day_name}: {', '.join(classes_scheduled)}")

# Run the evolution
population, generations = run_evolution(
    populate_func=partial(generate_population, size=100),
    fitness_func=partial(fitness, classes=ClassesList, days=DaysList),
    fitness_limit=60,  # Set a high limit to let it run for all generations
    generation_limit=1000,
)

print(f"Number of generations: {generations}")
print("Best schedule found:")
print_schedule(population[0], ClassesList, DaysList)
print(f"Fitness: {fitness(population[0], ClassesList, DaysList)}")

# Print details of the schedule
best_genome = population[0]
total_value = 0
total_duration = 0
schedule = genome_to_schedule(best_genome, ClassesList, DaysList)

for day in DaysList:
    print(f"\n{day.name} (Available: {day.available_duration} hours):")
    day_duration = 0
    day_value = 0
    for class_name in schedule[day.name]:
        class_info = next(c for c in ClassesList if c.name == class_name)
        print(f"  {class_info.name}: {class_info.duration} hours, value {class_info.value}")
        day_duration += class_info.duration
        day_value += class_info.value
    print(f"  Total: {day_duration} hours, value {day_value}")
    total_duration += day_duration
    total_value += day_value

print(f"\nOverall total: {total_duration} hours, value {total_value}")