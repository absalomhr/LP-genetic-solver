import random # Used for  generating random real and natural numbers
from math import log # Logarithm of x
from math import ceil # Smalles integer not less than x
from tabulate import tabulate # Library that makes printing a table easy
import collections # For counting frequencies of appearance
import operator # For sorting a dictionary by value
# This libraries are used for stoping the execution of the program
import os
import time
from datetime import datetime
from threading import Timer

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
    #print (values)
    for i in range(len(restrictions)):
        result = 0
        for j in range(n_variables):
            result += values [j] * restrictions [i][j]
        # print("Restiction: " + str(i+1))
        # print (values)
        # print (result)
        if restrictions[i][n_variables] == "le" and not (result <= restrictions[i][-1]):
            return False
        elif restrictions[i][n_variables] == "ge" and not (result >= restrictions[i][-1]):
            return False
        elif restrictions[i][n_variables] == "eq":
            print("is " + str(result) + " == " + str(restrictions[i][-1]), end = '\r')       
            valueNeeded = restrictions[i][-1]
            upperError = valueNeeded * (1.05)
            lowerError = valueNeeded * (0.95)
            if not (result >= lowerError):
                return False
            if not (result <= upperError):
                return False
    return True

# Function that returns a list of headers for tabulation
def getHeaders (n):
    my_headers = ["Vector"]
    for i in range (n):
        my_headers.append ("X"+str(i))
    my_headers.append("Z"); my_headers.append("%Z"); my_headers.append("%Z acc");
    my_headers.append("rand[0,1]"); my_headers.append("Vector *")
    return my_headers

# Function that generates a valid population and the values for each genotype
# If the genotypes are valid, we don't have to verify them, just retrieve the variable values
def generatePopulation (mjs, limits, restrictions, population, n_variables, genotypes, valid=False):
    result = []
    n_genotypes_generated = 0
    # Generating the first population and adding it to the result table
    mjs_sum = sum(mjs)
    if not valid:
        valid_values = False
        for i in range(population):
            while not valid_values:
                t_genotype = generate_genotype (mjs_sum)
                n_genotypes_generated += 1
                t_values = calculate_values (t_genotype, limits, mjs, n_variables)
                valid_values = areValuesValid (t_values, restrictions, n_variables)
                # If the values are valid we can add the genotype to the
                # population, and start to fill the result table
                if valid_values:
                    print ("\ngenotipo valido")
                    genotypes.append(t_genotype)
                    result.append([])
                    result[i].append(i + 1)
                    result [i] += t_values
                    valid_values = False
                    break
                # print ("Genotypes generated in first population: " + str(n_genotypes_generated), end = '\r')
    return result

# This function calculates the rest of the columns in the result table
# and returns the las column as a list for further calculation
# of the next iteration of the algorithm
def calculateIteration (vectors, genotypes, result_table, z_function, population, n_variables, mjs, limits, firsIteration=False, lastIteration=False):
    # If this is the first iteration we have to generate the population
    if firsIteration:
        result_table = generatePopulation (mjs, limits, restrictions, population, n_variables, genotypes)
    else:
        result_table = evaluateResults (vectors, limits, mjs, genotypes, z_function, population, n_variables)

    # Calculate all the Z functions for each geenotype
    for i in range(population):
        current = 0
        for j in range(n_variables):
            current += result_table[i][j + 1] * z_function[j]
            #current += math.e ** (-1 * ((result_table[i][j + 1]) ** 2) / 2) / math.sqrt(2*math.pi)
        result_table [i].append(current)
    
    # # Sum of all Z's
    z_sum = 0
    for i in range (population):
        z_sum += result_table[i][n_variables + 1]
    
    # %Z's, %Z acc, rand [0,1]
    # Point 4, 5 and 6 of the result_table   
    for i in range (population):
        result_table[i].append (result_table[i][n_variables + 1] / z_sum) # Z%
        if i == 0:
            result_table[i].append(result_table[i][n_variables + 2]) # Z% accummulated
        else:
            result_table[i].append(result_table[i][n_variables + 2] + result_table[i - 1][n_variables + 3])
        result_table[i].append(random.uniform(0,1)) # Random number between 0 and 1
    
    # Calculation of the "winners" vector
    # Each random number falls into a range of accumulated percentage
    vectors = []
    for i in range (population):
        ran_num = result_table[i][n_variables + 4] # The number generated before
        for j in range (population): # Try to fit the number in each range
            if j == 0: # first range [0, first_percentage]
                lower = 0; upper = result_table[j][n_variables + 3]
            else:
                lower = result_table[j - 1][n_variables + 3]; upper = result_table[j][n_variables + 3] # the rest of the ranges
            if lower <= ran_num <= upper: # if the number falls between a range we take the highest value
                result_table[i].append(j + 1)
                vectors.append(j + 1)
    print("\n" + tabulate(result_table, getHeaders(n_variables)))
    print ("Sum of Z's: " + str(z_sum))

    if lastIteration:
        zs = []
        for i in range(population):
            zs.append(result_table[i][n_variables + 1])
        print("Best Z: " + str(max(zs)) + " Vector: " + str(zs.index(max(zs)) + 1))
        print("Most common vector: " + str(max(set(vectors), key=vectors.count)))
    return vectors

# Function that evaluates whether all the values in a list are equal
def all_same (items):
    return all(x == items[0] for x in items)

# Receives a sorted list of elements, returns a dictionary of {item : appearance_count}
def calculate_frequency(items):
    return collections.Counter (items)

# Function that mutates (changes one random bit) of the current genotype
def mutate (vector):
    rand_index = random.randint (0, len (vector) - 1)
    # We use a list to alter the string, since strings are inmutable
    #print("m")
    #print(vector)
    temp_l = list (vector)
    if vector [rand_index] == "0":
        temp_l [rand_index] = "1"
    else:
        temp_l [rand_index] = "0"
    new_vector = "".join (temp_l)
    #print(new_vector)
    return new_vector

def cross (v1, v2):
    #print("c")
    #print(v1)
    #print(v2)
    rand_index = random.randint (1, len (v1) - 1)
    res = v1[:rand_index] + v2[rand_index:]
    #print(res)
    return res

# Function that generates the next population (genotypes)
# Using mutation or crossing
def evaluateResults (vectors, limits, mjs, genotypes, z_function, population, n_variables):
    result = []
    # Case where only one vector is the winner
    # That vector passes to the next generation
    # The rest are mutations of that vector
    if (all_same(vectors) and len(vectors) > 0):
        # Passing the winner vector
        genotypes [0] = genotypes [vectors[0] - 1]
        result.append([])
        result [0].append(1)
        result [0] += calculate_values (genotypes[0], limits, mjs, n_variables)
        for i in range (1, population):
            valid_values = False
            while not valid_values:
                t_genotype = mutate (genotypes[0])
                t_values = calculate_values (t_genotype, limits, mjs, n_variables)
                valid_values = areValuesValid (t_values, restrictions, n_variables)
                # If the values are valid we can add the genotype to the
                # population, and start to fill the result table
                if valid_values:
                    genotypes[i] = t_genotype
                    result.append([])
                    result[i].append(i + 1)
                    result [i] += t_values
                    valid_values = False
                    break
        return result
    genotypes_copy = genotypes [::] # Preservation of the originals for operations
    freq_dic = calculate_frequency(sorted(vectors)) # Dictionary of {vector_index : frequency_of_appearance}
    # Case where all the vectors have equal frequency of appearance
    # They all pass to the next generation
    if all_same(list(freq_dic.values())) and len(freq_dic) == population:
        for i in range(population):
            genotypes[i] = genotypes_copy [vectors[i] - 1]
            t_values = calculate_values (genotypes[i], limits, mjs, n_variables)
            result.append([])
            result[i].append(i + 1)
            result [i] += t_values
        return result
    # None of the other cases
    # We have one or more winners
    # The winers pass to the next generation
    # The rest are mutations or crossings of the winners
    sorted_freq_dic = sorted(freq_dic.items(), key=operator.itemgetter(1), reverse=True)
    winners = [] # vectors that pass to the next generation
    # for i in range(len(sorted_freq_dic) - 1):
    #     if i == 0:
    #         winners.append(sorted_freq_dic[0][0]) # vector with most appearances
    #     elif sorted_freq_dic[i][1] == sorted_freq_dic[i-1][1]: # the next vector has the same appearances
    #         winners.append(sorted_freq_dic[i][0])
    #     else: # the next vector has'nt the same appearances, so we stop the loop
    #         break
    for i in range(len(sorted_freq_dic)):
        winners.append(sorted_freq_dic[i][0])
    #print(winners)
    for i in range(len(winners)): # The winner vectors pass to the next generation
        genotypes [i] = genotypes_copy [winners[i] - 1]
        result.append([])
        result[i].append(i + 1)
        result[i] += calculate_values (genotypes [i], limits, mjs, n_variables)
    for i in range(len(winners), population): # The rest of the vectors are mutations or crossings of the winners
        valid_values = False
        while not valid_values:
            if len(winners) > 1:
                if random.randint(0, 1) == 0: # 0: mutate, 1: crossings
                    t_genotype = mutate (genotypes_copy[random.randint(0, len(winners) - 1)])
                else:
                    v1 = v2 = 0
                    while v1 == v2:
                        v1 = random.randint(0, len(winners) - 1)
                        v2 = random.randint(0, len(winners) - 1)
                    t_genotype = cross (genotypes_copy[winners[v1] - 1], genotypes_copy[winners[v2] - 1])
            else:
                t_genotype = mutate (genotypes_copy[winners[0] - 1])
            t_values = calculate_values (t_genotype, limits, mjs, n_variables)
            valid_values = areValuesValid (t_values, restrictions, n_variables)
            if valid_values:
                result.append([])
                result[i].append(i + 1)
                result[i] += t_values
                genotypes[i] = t_genotype
                break
    return result

# Function that stops the execution of the program after certain time
def exitfunc():
    print ("Exit Time: " + str(datetime.now()))
    os._exit(0)
Timer(300, exitfunc).start() # exit in 120 seconds (2 minutes)

# The coeficcients of the function that we have to maximize or minimize
# z_function = [-1, -1]
# z_function = [-1, -1, -1]
z_function = [1, -1, 1, 1]
# z_function = [1, 1, -2, 1]

# The inequations that need to be fulfilled at all times
# of the form [[coeficcients, comparison sign, constant]
# restrictions = [[2, 1, "le", 20], [1, 1, "ge", 10], [1, 0, "ge", 0], [0, 1, "ge", 0]]
# restrictions = [[1, 0, 1, "le", 50], [2, 1, 0, "le", 75], [1, 0, -1, "ge", 10], [1, 0, 0, "ge", 0], [0, 1, 0, "ge", 0], [1, 0, 0, "ge", -5]]
restrictions = [[1, 1, 0, 0, "le", 30], [1, 0, 0, 1, "le", 40], [1, 1, 1, 1, "eq", 100], [1, 0, 0, 0, "ge", 0], [0, 1, 0, 0, "ge", 0], [0, 0, 1, 0, "ge", 0], [0, 0, 0, 1, "ge", 0]]
# restrictions = [[1, 0, 1, 0, "le", 50], [0, 1, 0, 1, "le", 75], [1, 0, 0, 0, "ge", 10], [0, 1, 0, 1, "le", 100], [0, 0, 2, 1, "ge", 30], [1, 0, 0, 0, "ge", 0], [0, 1, 0, 0, "ge", 0], [0, 0, 1, 0, "ge", 0], [0, 0, 0, 1, "ge", 0]]

# Quantity of genotypes for each population
population = 10
# See mathematical formula on the readme
precission_bits = 0
# Max number of iterations (generations) before stoping
iterations = 5
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
# List where we store the indexes of the "winner" vectors
vectors = []

n_variables = len(z_function) # How many variables are in our system
limits = get_limits(restrictions, n_variables)
print("The limits of each variable are: " + str(limits))
mjs = get_mjs(precission_bits, limits, n_variables)
print("The mj's of each variable are: " + str(mjs))
# Calculating the result table of each iteration
for i in range (iterations):
    print("Iteration " + str(i+1) + ":")
    if i == 0:
        vectors = calculateIteration(vectors, genotypes, result_table, z_function, population, n_variables, mjs, limits, firsIteration=True)
    elif i == iterations - 1:
        vectors = calculateIteration(vectors, genotypes, result_table, z_function, population, n_variables, mjs, limits, lastIteration=True)
    else:
        vectors = calculateIteration(vectors, genotypes, result_table, z_function, population, n_variables, mjs, limits)
    #print ("vectors: " + str(vectors))
    #print ("genotypes: " + str(genotypes))
os._exit(0)
