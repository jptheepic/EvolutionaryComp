# This is my first test at creating an ec to a very easy computational problem
# Here are things we will need, an environment, fitness function, parent selection, mutation?
# This project will solve for the optimal values of x and y  for the problem of 
# 3x^2 + 4y +12 =50 
# fitness is evaluated by how close the raw answer is  to the expected answer of 50
# The population generation seems very random, id like to learn new ways to do this selection process more 
# effectivly. 

import random
class EvolutionaryPolynomialSolver:
  def __init__(self, population_size: int):
    self.population=[]
    self.population_size=population_size
    self.threshold=5
    for i in range(population_size):
      rnd_x = 0
      rnd_y =0
      self.population.append({"x":random.randrange(0,1000),"y":random.randrange(0,1000),"fitness":0}) 
    self.fitness()

  def problem(self, indiv: dict):
    sol = 3*indiv['x']**2 + 4*indiv['y'] + 12 -50
    return sol

  def fitness(self):
    for indiv in self.population:
      fit = self.problem(indiv)
      if fit ==0:
        indiv['fitness'] = 9999999999
      else:
        indiv['fitness'] = abs(1/fit)

  def mutate_population(self):
    #sort the population by fitness
    sorted_pop = sorted(self.population, key=lambda x: x['fitness'],reverse=True)
    # Choose top 5 parents
    choosen_parents = sorted_pop[:int(self.population_size*.1)]
    # Generate new population by using parent solution
    # Using kind of a random generation based off parent parameters to kind of guesscloser to the population
    # First the random parent is picked at ramdom
    # Then a solution is generated between 0 and the current parameter with a threshold dependent on fitness
    self.population = []
    for i in range(self.population_size):
      parent = choosen_parents[random.randint(0,len(choosen_parents)-1)]
      threshold = self.threshold
      # Create new population
      # Will choose a random parent from the top 5% of the population and generate a random number within the threshold
      self.population.append({"x":random.uniform(parent['x']-threshold,parent['x']+threshold),"y":random.uniform(parent['y']-threshold,parent['y']+threshold),"fitness":0}) 
      

  def experiment(self, interations:int):
    #inital fitness assesment
    for i in range(interations):
      self.mutate_population()
      self.fitness()
      # Decreacing threshold through iterations as we get closer to a solution
      # hopfully this will help decrease the range of randomization as we get closer to an optimal solution
      # self.threshold = self.threshold - (1/self.threshold)
      print(f"Generation {i}")

      # Search pop for solution, set 10 as the acceptable fitness threshold for a solution
      total_fit =0
      for indiv in self.population:
        if indiv['fitness'] >= 10:
          print("Solution Found!!!!")
          print(indiv)
          return indiv
    best_ans = sorted(self.population, key=lambda x: x['fitness'],reverse=True)[0]
    print("No optimal solution found:")
    print(best_ans)
    return best_ans  


if __name__ == '__main__':
  solver = EvolutionaryPolynomialSolver(population_size=50)
  sol = solver.experiment(interations=100)
  print(3*sol['x']**2 + 4*sol['y'] + 12)
