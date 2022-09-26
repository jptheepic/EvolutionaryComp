# This will be used to create an EC to
class BootstrapEvolution:
    def __init__(self, population_size: int()):
        ...

    def random_indiv(self):
        ...

    def fitness(self):
        ...

    def select_parents(self):
        ...

    def recombine():
        ...

    def mutate():
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
    experiment = BootstrapEvolution(population_size=10)
