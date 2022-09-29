
import sys
import string
import random
from typing import TypedDict

class Individual(TypedDict):
    genome: str
    fitness: int
Population = list[Individual]


def initialize_individual(genome: str, fitness: int) -> Individual:
    """
    Purpose:        Create one individual
    Parameters:     genome as string, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a dict[str, int]
    Modifies:       Nothing
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')

def initialize_pop(objective: str, pop_size: int) -> Population:
    """
    Purpose:        Create population to evolve
    Parameters:     Goal string, population size as int
    User Input:     no
    Prints:         no
    Returns:        a population, as a list of Individuals
    Modifies:       Nothing
    Calls:          random.choice, string.ascii_letters, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')

def recombine_pair(parent1: Individual, parent2: Individual) -> Population:
    """
    Purpose:        Recombine two parents to produce two children
    Parameters:     Two parents as Individuals
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, random.choice, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')
    
def recombine_group(parents: Population, recombine_rate: float) -> Population:
    """
    Purpose:        Recombines a whole group, returns the new population
    Parameters:     genome as string, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        New population of children
    Modifies:       Nothing
    Calls:          Basic python, recombine pair
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')

def mutate_individual(parent: Individual, mutate_rate: float) -> Individual:
    """
    Purpose:        Mutate one individual
    Parameters:     One parents as Individual, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')
    
def mutate_group(children: Population, mutate_rate: float) -> Population:
    """
    Purpose:        Mutates a whole Population, returns the mutated group
    Parameters:     Population, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, mutate_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')
def evaluate_individual(objective: str, individual: Individual) -> None:
    """
    Purpose:        Computes and modifies the fitness for one individual
    Parameters:     Objective string, One Individual
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The individual (mutable object)
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')
    
def evaluate_group(objective: str, individuals: Population) -> None:
    """
    Purpose:        Computes and modifies the fitness for population
    Parameters:     Objective string, Population
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The Individuals, all mutable objects
    Calls:          Basic python, evaluate_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')

def rank_group(individuals: Population) -> None:
    """
    Purpose:        Create one individual
    Parameters:     Population of Individuals
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The population's order (a mutable object)
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')

def parent_select(individuals: Population, number: int) -> Population:
    """
    Purpose:        Choose parents in direct probability to their fitness
    Parameters:     Population, the number of individuals to pick.
    User Input:     no
    Prints:         no
    Returns:        Sub-population
    Modifies:       Nothing
    Calls:          Basic python, random.choices (hint)
    Tests:          ./unit_tests/*
    Status:         Do this one!
    """
    print('Delete this and write your code')
    
def survivor_select(individuals: Population, pop_size: int) -> Population:
    """
    Purpose:        Picks who gets to live!
    Parameters:     Population, and population size to return.
    User Input:     no
    Prints:         no
    Returns:        Population, of pop_size
    Modifies:       Nothing
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         
   
    """
    print('Delete this and write your code')

def evolve(objective: str, pop_size: int) -> Population:
    """
    Purpose:        A whole EC run, main driver
    Parameters:     The evolved population of solutions
    User Input:     No
    Prints:         Updates every time fitness switches.
    Returns:        Population
    Modifies:       Various data structures
    Calls:          Basic python only, all your functions
    Tests:          ./stdio_tests/* and ./arg_tests/
    Status:         Giving you this one.
    """
    population = initialize_pop(objective=objective, pop_size=pop_size)
    evaluate_group(objective=objective, individuals=population)
    rank_group(individuals=population)
    best_fitness = population[0]["fitness"]
    perfect_fitness = len(objective)
    counter = 0
    while best_fitness < perfect_fitness:
        counter += 1
        parents = parent_select(individuals=population, number=80)
        children = recombine_group(parents=parents, recombine_rate=0.8)
        mutate_rate = (1 - (best_fitness / perfect_fitness)) / 5
        mutants = mutate_group(children=children, mutate_rate=mutate_rate)
        evaluate_group(objective=objective, individuals=mutants)
        everyone = population + mutants
        rank_group(individuals=everyone)
        population = survivor_select(individuals=everyone, pop_size=pop_size)
        if best_fitness != population[0]["fitness"]:
            best_fitness = population[0]["fitness"]
            print("Iteration number", counter, "with best individual", population[0])
    return population
    
if __name__ == "__main__":
    # Execute doctests to protect main:
    import doctest
    import json
    # This seeds, so can be commented for random runs
    doctest.testmod()
    if len(sys.argv) == 3:
        with open(file=sys.argv[1]) as finput:
            obj_name = finput.readlines()
            OBJECTIVE = obj_name[0].strip()
            POP_SIZE = int(obj_name[1])
        with open(file=sys.argv[2], mode="w") as foutput:
            population = evolve(OBJECTIVE, POP_SIZE)
            foutput.write(json.dumps(population) + "\n")
    else:
        OBJECTIVE = input("What string would you like to evolve?\n")
        POP_SIZE = int(input("How many individuals would you like to evolve?\n"))
        population = evolve(OBJECTIVE, POP_SIZE)
