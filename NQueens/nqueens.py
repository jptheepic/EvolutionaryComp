import sys
import random
from typing import TypedDict
from board_visualization import draw_board


class Individual(TypedDict):
    genome: list
    fitness: int


Population = list[Individual]


def initialize_individual(genome: list, fitness: int) -> Individual:
    """
    Purpose:        Create one individual
    Parameters:     genome as list, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a dict[list, int]
    Modifies:       Nothing
    Calls:          Basic python only
    """
    return Individual(genome=genome, fitness=fitness)


def initialize_pop(board_size: str, pop_size: int) -> Population:
    """
    Purpose:        Create population to evolve
    Parameters:     Goal string, population size as int
    User Input:     no
    Prints:         no
    Returns:        a population, as a list of Individuals
    Modifies:       Nothing
    Calls:          random.choice, string.ascii_letters, initialize_individual
    """
    population = []
    lst = range(0, board_size)
    for i in range(pop_size):
        population.append(
            initialize_individual(genome=random.sample(lst, k=board_size), fitness=100)
        )
    return population


def recombine_pair(parent1: Individual, parent2: Individual) -> Population:
    """
    Purpose:        Recombine two parents to produce two children
    Parameters:     Two parents as Individuals
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[list, int]
    Modifies:       Nothing
    Calls:          Basic python, random.choice, initialize_individual
    """
    # Single point crossover
    length = len(parent1["genome"])
    # randomly select crossover point within the len of the list
    crossover_point = random.randint(0, length - 1)
    c_genome1 = (
        parent1["genome"][:crossover_point] + parent2["genome"][crossover_point:]
    )
    c_genome2 = (
        parent2["genome"][:crossover_point] + parent1["genome"][crossover_point:]
    )
    return [
        initialize_individual(c_genome1, 100),
        initialize_individual(c_genome2, 100),
    ]


def recombine_group(parents: Population, recombine_rate: float) -> Population:
    """
    Purpose:        Recombines a whole group, returns the new population
    Parameters:     genome as list, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        New population of children
    Modifies:       Nothing
    Calls:          Basic python, recombine pair
    """
    new_pop = []
    pop = iter(parents)
    for i in pop:
        if random.random() <= recombine_rate:
            new_pop.extend(recombine_pair(i, next(pop)))
        else:
            new_pop.extend([i, next(pop)])
    return new_pop


def mutate_individual(parent: Individual, mutate_rate: float) -> Individual:
    """
    Purpose:        Mutate one individual
    Parameters:     One parents as Individual, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[list, int]
    Modifies:       Nothing
    Calls:          Basic python, initialize_individual
    """
    # Generate two random pos in the arr to swap.
    if random.random() <= mutate_rate:
        genome = parent["genome"]
        pos = random.sample(range(1, len(genome)), 2)
        # SWap the two picked positions
        genome[pos[0]], genome[pos[1]] = genome[pos[1]], genome[pos[0]]
        indiv = Individual(genome=genome, fitness=100)
    else:
        indiv = parent
    return indiv


def mutate_group(children: Population, mutate_rate: float) -> Population:
    """
    Purpose:        Mutates a whole Population, returns the mutated group
    Parameters:     Population, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[list, int]
    Modifies:       Nothing
    Calls:          Basic python, mutate_individual
    """
    new_population = []
    for indiv in children:
        new_population.append(mutate_individual(parent=indiv, mutate_rate=mutate_rate))
    return new_population


def evaluate_individual(individual: Individual) -> None:
    """
    Purpose:        Computes and modifies the fitness for one individual
    Parameters:     Objective string, One Individual
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The individual (mutable object)
    Calls:          Basic python only
    """
    left_diagional = []
    right_diagional = []
    for col, row in enumerate(individual["genome"]):
        row = int(row)
        if row - col == 0:
            left_diagional.append(0)
        elif row - col < 0:
            left_diagional.append((row - col))
        elif (row - col) > 0:
            left_diagional.append(row - col)
        right_diagional.append(row + col)
    right_fit = sum([right_diagional.count(i) > 1 for i in right_diagional])
    left_fit = sum([left_diagional.count(i) > 1 for i in left_diagional])
    rpt_fit = sum([individual["genome"].count(i) > 1 for i in individual["genome"]])

    # for every confict found add a point to fitness
    individual["fitness"] = right_fit + left_fit + rpt_fit


def evaluate_group(individuals: Population) -> None:
    """
    Purpose:        Computes and modifies the fitness for population
    Parameters:     Objective string, Population
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The Individuals, all mutable objects
    Calls:          Basic python, evaluate_individual
    """
    for idx in range(len(individuals)):
        evaluate_individual(individual=individuals[idx])


def rank_group(individuals: Population) -> None:
    """
    Purpose:        Create one individual
    Parameters:     Population of Individuals
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The population's order (a mutable object)
    Calls:          Basic python only
    """
    for idx, indiv in enumerate(
        sorted(individuals, key=lambda x: x["fitness"], reverse=False)
    ):
        individuals[idx] = indiv


def parent_select(individuals: Population, number: int) -> Population:
    """
    Purpose:        Choose parents in direct probability to their fitness
    Parameters:     Population, the number of individuals to pick.
    User Input:     no
    Prints:         no
    Returns:        Sub-population
    Modifies:       Nothing
    Calls:          Basic python, random.choices 
    """
    return random.choices(
        individuals, weights=[indiv["fitness"] for indiv in individuals], k=number
    )


def survivor_select(individuals: Population, pop_size: int) -> Population:
    """
    Purpose:        Picks who gets to live!
    Parameters:     Population, and population size to return.
    User Input:     no
    Prints:         no
    Returns:        Population, of pop_size
    Modifies:       Nothing
    Calls:          Basic python only, rank_group      
   
    """
    rank_group(individuals=individuals)
    return individuals[:pop_size]


def evolve(board_size: int, pop_size: int) -> Population:
    """
    Purpose:        A whole EC run, main driver
    Parameters:     The evolved population of solutions
    User Input:     No
    Prints:         Updates every time fitness switches.
    Returns:        Population
    Modifies:       Various data structures
    Calls:          Basic python only, all functions
    """
    population = initialize_pop(board_size=board_size, pop_size=pop_size)
    evaluate_group(individuals=population)
    rank_group(individuals=population)
    best_fitness = population[0]["fitness"]
    perfect_fitness = 0
    # This will keep track of how many iterations occur without improvemnet
    # This will affect the mutation rate
    no_improvement = 0.4
    counter = 0
    while best_fitness > perfect_fitness:
        counter += 1
        parents = parent_select(individuals=population, number=80)
        children = recombine_group(parents=parents, recombine_rate=0.8)
        mutate_rate = no_improvement
        # Mustation rate will increase as no improvement occurs
        mutants = mutate_group(children=children, mutate_rate=mutate_rate)
        evaluate_group(individuals=mutants)
        everyone = population + mutants
        rank_group(individuals=everyone)
        population = survivor_select(individuals=everyone, pop_size=pop_size)
        # Uncomment this to see all iterations of the board.. will pop up a lot
        # draw_board(population[0], counter)
        if population[0]["fitness"] < 5:
            draw_board(population[0], counter)
        if best_fitness != population[0]["fitness"]:
            best_fitness = population[0]["fitness"]
            print("Iteration number", counter, "with best individual", population[0])
            draw_board(population[0], counter)
            no_improvement = 0.4
        else:
            no_improvement += 0.001
    return population


if __name__ == "__main__":
    # BOARD_SIZE = input("What size of board would you like to evolve?\n")
    # POP_SIZE = int(input("How many individuals would you like to evolve?\n"))

    BOARD_SIZE = 100
    POP_SIZE = 100
    population = evolve(BOARD_SIZE, POP_SIZE)
