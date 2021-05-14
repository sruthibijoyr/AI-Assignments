from time import process_time 
import random
from random import choices

class Problem:
	def __init__(self):
		self.goal = 1

	def generatePopulation(self,k):
		population = [] 
		for i in range(k):
			individual = []
			for j in range(8):
				individual.append(random.randint(0,7))
			population.append(individual)
		return population

	def fitness_func(self,individual):
		attacks = 0
		for r1 in range(8):
			c1 = individual[r1]
			for r2 in range(8):
				c2 = individual[r2]
				if (c1,r1) != (c2,r2):
					if r1 == r2 or c1 == c2 or ((r1 - c1) == (r2 - c2)) or ((r1 + c1) == (r2 + c2)):
						attacks+=1
		return (1/(1+attacks))

	def fitEnough(self,population):
		for individual in population:
			if self.fitness_func(individual) == self.goal:
				return individual
		return None

def reproduce(x,y):
	n = len(x)
	c = random.randint(0,n-1)
	return x[:c]+y[c:]


def randomSelection(population, fitness_func):
	fitness_vals = list(map(fitness_func, population))
	total = sum(fitness_vals)
	fitness_vals = list(map(lambda x: x/total, fitness_vals))
	selected = choices(population,fitness_vals)
	return selected[0]

def mutate(individual):
	n = len(individual)
	row = random.randint(0,n-1)
	col = random.randint(0,n-1)
	individual[row] = col
	return individual

def timeElapsed(t1):
	t2 = process_time()
	if t2 - t1 > 300:
		return True


def geneticAlgorithm(problem,k,prob_mut):
	population = problem.generatePopulation(k)
	start = process_time()
	while True:
		new_population = []
		for i in range(len(population)):
			x = randomSelection(population,problem.fitness_func)
			y = randomSelection(population,problem.fitness_func)
			child = reproduce(x,y)
			if random.uniform(0,1) < prob_mut:
				child = mutate(child)

			new_population.append(child)
		population = new_population[:]

		individual = problem.fitEnough(population)

		if individual:
			return individual
		if timeElapsed(start) == True:
			return None

#------------Empertical Analysis-------------

problem = Problem()

size = [4,8,10,20]
prob_mut = [0.01, 0.05, 0.1]

for k in size:
	for p in prob_mut:
		time_taken = 0
		fails = 0
		for m in range(5):	
			start = process_time()
			res = geneticAlgorithm(problem,k,p)
			if res == None:
				print("\n\n------------------------- k = ",k,", p = ",p,"Iteration = ",m+1," ------------------------\nNo safe configuration found within time limit (300s) ")
				fails += 1
				continue;
			stop = process_time()
			time_takenm = stop - start
			time_taken += time_takenm
			print("\n\n------------------------- k = ",k,", p = ",p,"Iteration = ",m+1," ------------------------\nSafe configuration: ",res,", Time Elapsed: ",time_takenm," seconds")
		avg_time = time_taken/(5-fails)
		print("\nAverage time taken for k = ",k,", p = ",p," : ",avg_time," seconds")
		print("\n************************************************************************************************\n")


'''
OUTPUT:

------------------------- k =  4 , p =  0.01 Iteration =  1  ------------------------
Safe configuration:  [1, 4, 6, 3, 0, 7, 5, 2] , Time Elapsed:  1.90625  seconds


------------------------- k =  4 , p =  0.01 Iteration =  2  ------------------------
Safe configuration:  [7, 1, 4, 2, 0, 6, 3, 5] , Time Elapsed:  32.796875  seconds


------------------------- k =  4 , p =  0.01 Iteration =  3  ------------------------
Safe configuration:  [3, 7, 4, 2, 0, 6, 1, 5] , Time Elapsed:  6.875  seconds


------------------------- k =  4 , p =  0.01 Iteration =  4  ------------------------
Safe configuration:  [5, 2, 4, 6, 0, 3, 1, 7] , Time Elapsed:  135.90625  seconds


------------------------- k =  4 , p =  0.01 Iteration =  5  ------------------------
Safe configuration:  [4, 1, 7, 0, 3, 6, 2, 5] , Time Elapsed:  78.46875  seconds

Average time taken for k =  4 , p =  0.01  :  51.190625  seconds

************************************************************************************************



------------------------- k =  4 , p =  0.05 Iteration =  1  ------------------------
Safe configuration:  [6, 3, 1, 7, 5, 0, 2, 4] , Time Elapsed:  11.203125  seconds


------------------------- k =  4 , p =  0.05 Iteration =  2  ------------------------
Safe configuration:  [3, 1, 4, 7, 5, 0, 2, 6] , Time Elapsed:  40.46875  seconds


------------------------- k =  4 , p =  0.05 Iteration =  3  ------------------------
Safe configuration:  [4, 1, 3, 5, 7, 2, 0, 6] , Time Elapsed:  3.796875  seconds


------------------------- k =  4 , p =  0.05 Iteration =  4  ------------------------
Safe configuration:  [3, 5, 0, 4, 1, 7, 2, 6] , Time Elapsed:  0.8125  seconds


------------------------- k =  4 , p =  0.05 Iteration =  5  ------------------------
Safe configuration:  [4, 0, 7, 5, 2, 6, 1, 3] , Time Elapsed:  25.890625  seconds

Average time taken for k =  4 , p =  0.05  :  16.434375  seconds

************************************************************************************************



------------------------- k =  4 , p =  0.1 Iteration =  1  ------------------------
Safe configuration:  [4, 1, 5, 0, 6, 3, 7, 2] , Time Elapsed:  4.40625  seconds


------------------------- k =  4 , p =  0.1 Iteration =  2  ------------------------
Safe configuration:  [1, 5, 7, 2, 0, 3, 6, 4] , Time Elapsed:  4.515625  seconds


------------------------- k =  4 , p =  0.1 Iteration =  3  ------------------------
Safe configuration:  [5, 7, 1, 3, 0, 6, 4, 2] , Time Elapsed:  1.75  seconds


------------------------- k =  4 , p =  0.1 Iteration =  4  ------------------------
Safe configuration:  [4, 6, 0, 2, 7, 5, 3, 1] , Time Elapsed:  5.140625  seconds


------------------------- k =  4 , p =  0.1 Iteration =  5  ------------------------
Safe configuration:  [4, 0, 7, 5, 2, 6, 1, 3] , Time Elapsed:  4.3125  seconds

Average time taken for k =  4 , p =  0.1  :  4.025  seconds

************************************************************************************************



------------------------- k =  8 , p =  0.01 Iteration =  1  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  8 , p =  0.01 Iteration =  2  ------------------------
Safe configuration:  [1, 4, 6, 3, 0, 7, 5, 2] , Time Elapsed:  177.1875  seconds


------------------------- k =  8 , p =  0.01 Iteration =  3  ------------------------
Safe configuration:  [2, 4, 1, 7, 0, 6, 3, 5] , Time Elapsed:  40.671875  seconds


------------------------- k =  8 , p =  0.01 Iteration =  4  ------------------------
Safe configuration:  [2, 6, 1, 7, 5, 3, 0, 4] , Time Elapsed:  70.390625  seconds


------------------------- k =  8 , p =  0.01 Iteration =  5  ------------------------
No safe configuration found within time limit (300s)

Average time taken for k =  8 , p =  0.01  :  96.08333333333333  seconds

************************************************************************************************



------------------------- k =  8 , p =  0.05 Iteration =  1  ------------------------
Safe configuration:  [3, 1, 7, 4, 6, 0, 2, 5] , Time Elapsed:  5.453125  seconds


------------------------- k =  8 , p =  0.05 Iteration =  2  ------------------------
Safe configuration:  [2, 0, 6, 4, 7, 1, 3, 5] , Time Elapsed:  6.1875  seconds


------------------------- k =  8 , p =  0.05 Iteration =  3  ------------------------
Safe configuration:  [1, 5, 7, 2, 0, 3, 6, 4] , Time Elapsed:  8.765625  seconds


------------------------- k =  8 , p =  0.05 Iteration =  4  ------------------------
Safe configuration:  [3, 1, 4, 7, 5, 0, 2, 6] , Time Elapsed:  54.671875  seconds


------------------------- k =  8 , p =  0.05 Iteration =  5  ------------------------
Safe configuration:  [4, 7, 3, 0, 6, 1, 5, 2] , Time Elapsed:  6.8125  seconds

Average time taken for k =  8 , p =  0.05  :  16.378125  seconds

************************************************************************************************



------------------------- k =  8 , p =  0.1 Iteration =  1  ------------------------
Safe configuration:  [3, 1, 6, 2, 5, 7, 0, 4] , Time Elapsed:  8.484375  seconds


------------------------- k =  8 , p =  0.1 Iteration =  2  ------------------------
Safe configuration:  [6, 2, 7, 1, 4, 0, 5, 3] , Time Elapsed:  2.53125  seconds


------------------------- k =  8 , p =  0.1 Iteration =  3  ------------------------
Safe configuration:  [5, 2, 0, 6, 4, 7, 1, 3] , Time Elapsed:  3.296875  seconds


------------------------- k =  8 , p =  0.1 Iteration =  4  ------------------------
Safe configuration:  [4, 1, 7, 0, 3, 6, 2, 5] , Time Elapsed:  9.75  seconds


------------------------- k =  8 , p =  0.1 Iteration =  5  ------------------------
Safe configuration:  [5, 3, 6, 0, 7, 1, 4, 2] , Time Elapsed:  11.28125  seconds

Average time taken for k =  8 , p =  0.1  :  7.06875  seconds

************************************************************************************************



------------------------- k =  10 , p =  0.01 Iteration =  1  ------------------------
Safe configuration:  [5, 2, 0, 7, 4, 1, 3, 6] , Time Elapsed:  14.375  seconds


------------------------- k =  10 , p =  0.01 Iteration =  2  ------------------------
Safe configuration:  [2, 0, 6, 4, 7, 1, 3, 5] , Time Elapsed:  4.78125  seconds


------------------------- k =  10 , p =  0.01 Iteration =  3  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  10 , p =  0.01 Iteration =  4  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  10 , p =  0.01 Iteration =  5  ------------------------
Safe configuration:  [3, 7, 0, 4, 6, 1, 5, 2] , Time Elapsed:  132.328125  seconds

Average time taken for k =  10 , p =  0.01  :  50.494791666666664  seconds

************************************************************************************************



------------------------- k =  10 , p =  0.05 Iteration =  1  ------------------------
Safe configuration:  [1, 5, 0, 6, 3, 7, 2, 4] , Time Elapsed:  57.4375  seconds


------------------------- k =  10 , p =  0.05 Iteration =  2  ------------------------
Safe configuration:  [4, 0, 7, 3, 1, 6, 2, 5] , Time Elapsed:  230.3125  seconds


------------------------- k =  10 , p =  0.05 Iteration =  3  ------------------------
Safe configuration:  [1, 3, 5, 7, 2, 0, 6, 4] , Time Elapsed:  2.28125  seconds


------------------------- k =  10 , p =  0.05 Iteration =  4  ------------------------
Safe configuration:  [2, 5, 1, 6, 0, 3, 7, 4] , Time Elapsed:  37.984375  seconds


------------------------- k =  10 , p =  0.05 Iteration =  5  ------------------------
Safe configuration:  [2, 7, 3, 6, 0, 5, 1, 4] , Time Elapsed:  0.625  seconds

Average time taken for k =  10 , p =  0.05  :  65.728125  seconds

************************************************************************************************



------------------------- k =  10 , p =  0.1 Iteration =  1  ------------------------
Safe configuration:  [3, 7, 4, 2, 0, 6, 1, 5] , Time Elapsed:  1.359375  seconds


------------------------- k =  10 , p =  0.1 Iteration =  2  ------------------------
Safe configuration:  [5, 3, 6, 0, 7, 1, 4, 2] , Time Elapsed:  23.015625  seconds


------------------------- k =  10 , p =  0.1 Iteration =  3  ------------------------
Safe configuration:  [4, 7, 3, 0, 6, 1, 5, 2] , Time Elapsed:  46.0625  seconds


------------------------- k =  10 , p =  0.1 Iteration =  4  ------------------------
Safe configuration:  [2, 4, 7, 3, 0, 6, 1, 5] , Time Elapsed:  2.0625  seconds


------------------------- k =  10 , p =  0.1 Iteration =  5  ------------------------
Safe configuration:  [3, 0, 4, 7, 1, 6, 2, 5] , Time Elapsed:  0.28125  seconds

Average time taken for k =  10 , p =  0.1  :  14.55625  seconds

************************************************************************************************



------------------------- k =  20 , p =  0.01 Iteration =  1  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  20 , p =  0.01 Iteration =  2  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  20 , p =  0.01 Iteration =  3  ------------------------
Safe configuration:  [3, 0, 4, 7, 1, 6, 2, 5] , Time Elapsed:  90.671875  seconds


------------------------- k =  20 , p =  0.01 Iteration =  4  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  20 , p =  0.01 Iteration =  5  ------------------------
No safe configuration found within time limit (300s)

Average time taken for k =  20 , p =  0.01  :  90.671875  seconds

************************************************************************************************



------------------------- k =  20 , p =  0.05 Iteration =  1  ------------------------
Safe configuration:  [2, 5, 7, 0, 4, 6, 1, 3] , Time Elapsed:  1.15625  seconds


------------------------- k =  20 , p =  0.05 Iteration =  2  ------------------------
Safe configuration:  [3, 5, 7, 2, 0, 6, 4, 1] , Time Elapsed:  36.25  seconds


------------------------- k =  20 , p =  0.05 Iteration =  3  ------------------------
Safe configuration:  [5, 2, 4, 7, 0, 3, 1, 6] , Time Elapsed:  267.59375  seconds


------------------------- k =  20 , p =  0.05 Iteration =  4  ------------------------
No safe configuration found within time limit (300s)


------------------------- k =  20 , p =  0.05 Iteration =  5  ------------------------
No safe configuration found within time limit (300s)

Average time taken for k =  20 , p =  0.05  :  101.66666666666667  seconds

************************************************************************************************



------------------------- k =  20 , p =  0.1 Iteration =  1  ------------------------
Safe configuration:  [4, 0, 7, 3, 1, 6, 2, 5] , Time Elapsed:  195.75  seconds


------------------------- k =  20 , p =  0.1 Iteration =  2  ------------------------
Safe configuration:  [5, 3, 6, 0, 7, 1, 4, 2] , Time Elapsed:  12.75  seconds


------------------------- k =  20 , p =  0.1 Iteration =  3  ------------------------
Safe configuration:  [2, 5, 3, 0, 7, 4, 6, 1] , Time Elapsed:  191.375  seconds


------------------------- k =  20 , p =  0.1 Iteration =  4  ------------------------
Safe configuration:  [5, 2, 0, 7, 3, 1, 6, 4] , Time Elapsed:  212.203125  seconds


------------------------- k =  20 , p =  0.1 Iteration =  5  ------------------------
Safe configuration:  [7, 3, 0, 2, 5, 1, 6, 4] , Time Elapsed:  0.59375  seconds

Average time taken for k =  20 , p =  0.1  :  122.534375  seconds

************************************************************************************************
'''