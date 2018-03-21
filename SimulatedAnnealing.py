import numpy as np  
import math
import random

def hillClimbing(step_sizes, x_start, x_low, x_high):
	iteration_list = []
	x_list = []
	y_list = []

	for start in x_start:
		for step_size in step_sizes:
			current_x = start 
			current_value = function(current_x)
			num_steps = 0
			x1 = current_x - step_size
			x2 = current_x + step_size 

			# if OOB
			if x1 < x_low:
				x1 = x_low 
			if x2 > x_high:
				x2 = x_high 

			value1 = function(x1)
			value2 = function(x2)

			while max(value1, value2) > current_value:
				num_steps = num_steps + 1

				if value1 > value2:
					current_x = x1
					current_value = value1
				else:
					current_x = x2
					current_value = value2 

				x1 = current_x - step_size
				x2 = current_x + step_size 
				value1 = function(x1)
				value2 = function(x2)

			iteration_list.append(num_steps)
			x_list.append(current_x)
			y_list.append(current_value)

	return y_list

def simulatedAnnealing(T, a, step_sizes, x_start, x_low, x_high):
	iteration_list = []
	x_list = []
	y_list = []


	for temp in T:
		for alpha in a:
			for start in x_start:
				for step_size in step_sizes:
					current_x = start 
					current_T = temp
					current_value = function(current_x)
					num_steps = 0
					x1 = current_x - step_size
					x2 = current_x + step_size 

					# if OOB
					if x1 < x_low:
						x1 = x_low 
					if x2 > x_high:
						x2 = x_high 

					value1 = function(x1)
					value2 = function(x2)

					while True:
						selected = False
						num_steps = num_steps + 1

						if current_T < 0.1:
							break

						# Randomly select next neighbor

						# SOLUTION 1: break from loop when we don't select any node

						# Select x1
						if random.uniform(0.0, 1.0) <= 0.5:
							# E_i > Emax
							if value1 > current_value:
								current_x = x1
								current_value = value1
								selected = True
							# Else, select with Boltzmann probability
							else:
								if boltzmannProb(current_value, value1, current_T):
									selected = True
									current_x = x1
									current_value = value1
									continue

						# Select x2
						else:
							# E_i > Emax
							if value2 > current_value:
								current_x = x2
								current_value = value2
								selected = True
							# Else, select with Boltzmann probability
							else:
								if boltzmannProb(current_value, value2, current_T):
									selected = True
									current_x = x2
									current_value = value2
									continue

						# multiply T by cooling schedule
						current_T = current_T * alpha

					iteration_list.append(num_steps)
					x_list.append(current_x)
					y_list.append(current_value)

	for i in y_list:
		print i 

	print "Y-------------------"

	for i in x_list:
		print i

	print "X-------------------"

	for i in iteration_list:
		print i

def boltzmannProb(E, E_i, T):
	return math.e ** (-(float(E)-E_i)/T)

def diceRoll(p):
	roll = random.uniform(0.0, 1.0)

	return True if roll <= p else False

def function(x):
	return math.sin(float(x**2)/2) * math.log(2) / math.log(x+4)

def main():
	x_start = [i for i in range(11)]
	step_sizes = np.arange(0.01, 0.101, 0.01)
	y_list = hillClimbing(step_sizes, x_start, 0, 10)

	# ---------------------

	step_sizes_2 = np.arange(0.01, 0.04, 0.01)
	T = [i for i in [4, 25, 100, 1000, 10000]]
	a = np.arange(0.80, 0.81, 0.02)

	simulatedAnnealing(T, a, step_sizes_2, x_start, 0, 10)


if __name__ == "__main__":
	main()
