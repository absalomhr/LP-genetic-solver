import random # Used for  generating random real and natural numbers
from math import log # Logarithm of x
from math import ceil # Smalles integer not less than x
from tabulate import tabulate # Library that makes printing a table easy

# Function that calculates the limits of each variable
# based on the restrictions given
def get_limits (restrictions, n_variables):
	# It will return a list with the limits
	# of each variable
	limits = []
	# All restrictions must bu fullfilled
	for i in range(n_variables): 
		temp_limits = [] # Holds all the limits of a variable so far
		for j in range(len(restrictions)):
			# ax = c
			# x = c / a
			if restrictions[j][i] != 0:
				temp_limits.append(restrictions[j][-1] / restrictions[j][i])
		# No-negativity case
		if 0 in limits:
			limits.append([0, max(temp_limits)])
		else:
			limits.append([min(temp_limits), max(temp_limits)])
	return limits

# Function that calculates the length of each fenotype
# that will make up each genotype that is in the population
# see the mathematical formula
def get_mjs (precission_bits, limits, n_variables):
	mjs = []
	for i in range(n_variables):
		res = (limits[i][1] - limits [i][0]) * (10 ** precission_bits)
		mjs.append(ceil (log(res) / log(2)))
	return mjs

# Function that generates one genotype
# It recieves the lenght of the genotype
# This is: the sum of the lengths of each mj
def generate_genotype (total_mj):
    genotype = "" # A genotype is a random string of 0's and 1's
    for i in range(total_mj):
    	genotype += str(random.randint(0, 1))
    return genotype

# Function that calculates the value of thr variables
# given the genotype of each variable
def calculate_values (genotype, limits, mjs, n_variables):
	values = []
	constant = 0
	for i in range(n_variables):
		if i == 0:
			fenotype = genotype [0:mjs[i]]
		else:
			fenotype = genotype [mjs[i - 1]:mjs[i - 1] + mjs[i]]
		constant = (limits[i][1] - limits[i][0]) / ((2 ** mjs[i]) - 1)
		values.append(limits[i][0] + (int(fenotype, 2) * constant))
	return values

# Function that determines whether the values
# ​​meet all the restrictions
def areValuesValid (values, restrictions, n_variables):
    for i in range(len(restrictions)):
        result = 0
        for j in range(n_variables):
            result += values [j] * restrictions [i][j]
        if restrictions[i][n_variables] == "le" and not (result <= restrictions[i][-1]):
                return False
        elif restrictions[i][n_variables] == "ge" and not (result >= restrictions[i][-1]):
                return False
        elif restrictions[i][n_variables] == "eq" and not (result == restrictions[i][-1]):
                return False
    return True


# The coeficcients of the function that we have to maximize or minimize
z_function = [1, 1]
# The inequations that need to be fulfilled at all times
# of the form [[coeficcients, comparison sign, constant]
restrictions = [[2, 4, "le", 125], [3, 5, "le", 100], [1, 0, "ge", 15], [0, 1, "ge", 0]]
# Quantity of genotypes for each population
population = 10000
# See mathematical formula on the readme
precission_bits = 2
# Max number of iterations (generations) before stoping
iterations = 0
# Limits of each variable
# Which values it can hold
limits = []
# Length of each fenotype that make up a genotype
mjs = []
# List containing the population of valid genotypes
genotypes = []
# The result table of each iteration
# Consisting of n_variables rows and these columns:
# 1. vector number
# 2. n_variables values
# 3. z_function evaluation with the values of point 2
# 4. Pencentage of current z_function evaluation
# in proportion to the sum of all of the z_function evaluations
# 5. Accumulated percentage
# 6. A random number beween [0,1]
# 7. The "winner" vector number
result_table = []

n_variables = len(z_function) # How many variables are in our system
limits = get_limits(restrictions, n_variables)
print("The limits of each variable are: " + str(limits))
mjs = get_mjs(precission_bits, limits, n_variables)
print("The mj's of each variable are: " + str(mjs))
# Generating the first population and adding it to the result table
mjs_sum = sum(mjs)
valid_values = False
for i in range(population):
	while not valid_values:
		t_genotype = generate_genotype (mjs_sum)
		t_values = calculate_values (t_genotype, limits, mjs, n_variables)
		valid_values = areValuesValid (t_values, restrictions, n_variables)
		# If the values are valid we can add the genotype to the
		# population, and start to fill the result table
		if valid_values:
			genotypes.append(t_genotype)
			result_table.append([])
			result_table[i].append(i + 1)
			result_table [i] += t_values
			valid_values = False
			break
print(tabulate(result_table))