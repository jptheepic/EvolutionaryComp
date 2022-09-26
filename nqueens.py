# This will be used to create an EC to

import random


class NQueensEvolution:
    def __init__(self, population_size, board_size: int()):
        """This function will initalize a random population, the inidividuals
    Will be represented by an array of N size, each row in the array will represent
    if a queen is in that column.

    Args:
        population_size (int): How large to create the population used for evoluation
        board_size (int): How large the board should be.
    """
        self.population = []
        self.board_size = board_size
        for i in range(population_size):
            self.population.append(self.random_indiv())
        print(self.population)

    def random_indiv(self):
        """Returns a random individual, this will create a random nonrepeating array
    of the size of the board and will fill this array with random non repearting numbers from 0-self.board_size

    Returns:
        list: list of the size of the board populated with random non-repeating integers
    """
        lst = range(1, self.board_size + 1)
        # This will do with replacement
        # return random.choices(lst,k=self.board_size)
        return random.sample(lst, k=self.board_size)

    def encode(self):
        #
        ...

    def decode(self):
        #
        ...

    def fitness(self):
        #
        ...

    def select_parents(self):
        # Evaluate fitness to pick the best parents, lets say the top blank% of the fitness
        ...

    def recombine():
        # Randomly pick a point in an array and then
        # Use singlepoint cross-combine
        ...

    def mutate():
        # Small statistical chance to flip two positions in the array
        # Should occur for 1% of the population size.
        ...

    def experiment(self):
        # evaluate each fitness
        self.fitness()
        Termination = False
        while Termination == False:
            # select parents
            self.select_parents()
            # recombine pairs of parents
            self.recombine()
            # Mutate the resulting offspring
            self.mutate()
            # Evaluate new Candidates
            self.fitness()
            # Check fitness for termination


if __name__ == "__main__":
    experiment = NQueensEvolution(population_size=10, board_size=8)
