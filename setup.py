from math import log
from math import ceil
from random import randint
from random import uniform
from tabulate import tabulate
import collections
import operator

iterations = 3
precission_bits = 2
population = 8
z_function = [1, 1]
restrictions = [[2, 4, "le", 125], [3, 5, "le", 100], [1, 0, "ge", 15], [0, 1, "ge", 0]]
#z_function = [1, 2, 3]
#restrictions = [[0, 3, 3, "ge", 80], [2, 5, 0, "ge", 125], [6, 8, 1, "le", 250], [1, 0, -1, "ge", 20], [1, 0, 0, "ge", 0], [0, 1, 0, "ge", 0], [0, 0, 1, "ge", 0]]
#z_function = [1, 2, -1, 1]
#restrictions = [[1, 0, 1, 0, "eq", 50], [1, 1, 0, 1, "le", 100], [0, 2, -1, 1, "le", 150], [1, 0, 0, 0, "ge", 10], [1,0,0,0,"ge",0], [0,1,0,0,"ge",0], [0,0,1,0,"ge",0], [0,0,0,1,"ge",0]]

# Caso 1: todos los vectores ganadores son iguales. Se pasa el ganador, los demas son mutaciones del ganador


def limit (restrictions, varpos):
    limits = []
    for i in range(len(restrictions)):
        var_coeff = restrictions[i][varpos]
        eq_res = restrictions[i][-1]
        if (var_coeff != 0):
            limits.append (eq_res / var_coeff)
    if 0 in limits:
        return (0, max(limits)) # no negativity case
    return (min(limits), max(limits))

def calc_mj (precission_bits, limits):
    return ceil (log ((limits[1] - limits [0]) * (10 ** precission_bits)) / log (2))

def generate_genotype (total_mj):
    genotype = ""
    for i in range (total_mj):
        genotype += str (randint(0,1))
    return genotype

def var_value (var_bin, upper_limit, lower_limit, mj):
    constant = (upper_limit - lower_limit) / ((2 ** mj) - 1)
    return lower_limit  + (var_bin * (constant))

def areValuesValid (values, restrictions): # Is the value of the variable valid for all restrictions
    n_variables = len (values)
    for i in range(len(restrictions)):
        res = 0
        current = 0
        #print("*** Restriction " + str (i + 1))
        for j in range(n_variables):
            current = values [j] * restrictions [i][j]
            res += current
            #print ("**** evaluation of X" + str(j) + ": " + str(restrictions [i][j]) + "*" + str(values [j]) + " = " + str (current))
        if restrictions[i][n_variables] == "le":
            #print ("***** Is " + str (res) + " <= " + str(restrictions[i][-1]))
            if not (res <= restrictions[i][-1]):
                return False
        elif restrictions[i][n_variables] == "ge":
            #print ("***** Is " + str (res) + " >= " + str(restrictions[i][-1]))
            if not (res >= restrictions[i][-1]):
                return False
        elif restrictions[i][n_variables] == "eq":
            #print ("***** Is " + str (res) + " = " + str(restrictions[i][-1]))
            if not (res == restrictions[i][-1]):
                return False
    return True

def isGenotypeValid (geno, z_function, mjs, limits, restrictions):
    temp_values = []
    for i in range(len(z_function)):
        if i == 0:
                fenotype = geno[0:mjs[i]]      
        else:
            fenotype = geno[mjs[i - 1]: mjs[i - 1] + mjs[i]]
        temp_values.append(var_value(int(fenotype, 2), limits[i][1], limits[i][0], mjs[i]))
    return (areValuesValid(temp_values, restrictions), temp_values)
                

def getHeaders (n):
    my_headers = ["Vector"]
    for i in range (n):
        my_headers.append ("X"+str(i))
    my_headers.append("Z"); my_headers.append("%Z"); my_headers.append("%Z acc");
    my_headers.append("rand[0,1]"); my_headers.append("Vector *")
    return my_headers

def calculateFirstIteration (result, z_function, v_result):
    n = len(result) # population
    m = len (z_function) # number of variables
    
    # Generate all the Z's
    for i in range(n):
        current = 0
        for j in range(m):
            current += result[i][j + 1] * z_function[j]
        result [i].append(current)
    
    # Sum of all Z's
    z_sum = 0
    for i in range (n):
        z_sum += result[i][m + 1]
    
    # %Z's, %Z acc, rand [0,1]    
    for i in range (n):
        result[i].append (result[i][m + 1] / z_sum)
        if i == 0:
            result[i].append(result[i][m + 2])
        else:
            result[i].append(result[i][m + 2] + result[i - 1][m + 3])
        result[i].append(uniform(0,1))
    
    # Which range for every random number
    for i in range (n):
        ran_num = result[i][m + 4]
        for j in range (n):
            if j == 0: # first range
                lower = 0; upper = result[j][m + 3]
            else:
                lower = result[j - 1][m + 3]; upper = result[j][m + 3]
            if lower <= ran_num <= upper: # if the number falls between a range we position in the highest
                result[i].append(j + 1)
                v_result.append(j + 1)
    print(tabulate(result, getHeaders(m)))
    print (z_sum)
def all_same(items):
    return all(x == items[0] for x in items)

def v_freq(items):
    res = collections.Counter (items)
    return res

def evaluateResults(v_result, genotypes, z_function, mjs, limits, restrictions):
    # Case where all the vectors are the same one
    if all_same(v_result):
        genotypes [0] = genotypes [v_result[0] - 1]
        for i in range (1, len(genotypes)):
            isValid = (False,[])
            while not isValid[0]:
                geno = mutate (genotypes[0])
                isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                if isValid[0]:
                    genotypes[i] = geno
                    break
    else:
        new_geno = genotypes [::]
        freq = v_freq(sorted(v_result))
        if all_same (list(freq.values())): # Equal frequency for each vector
            if len(freq) == len (genotypes): # All vectors have 1 frequency
                for i in range (len (genotypes)):
                    genotypes [i] = new_geno [v_result[i] - 1]
            else: # There are some vectors with equal frequency, the others have 0 frequency
                freq_k = list(freq.keys())
                #print (freq_k)
                n = len (freq)
                isValid = False
                for i in range (n):
                    genotypes [i] = new_geno [freq_k [i] - 1]
                for i in range (n, len(genotypes)):
                    option = randint (0,1)
                    if option == 0:
                        if (n > 1):
                            v1 = randint(1, n)
                            while True:
                                v2 = randint(1, n)
                                if v2 != v1:
                                    break
                            isValid = (False,[])
                            while not isValid[0]:
                                geno = cross (new_geno [freq_k [v1 - 1] - 1], new_geno [freq_k [v2 - 1] - 1])
                                isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                                if isValid[0]:
                                    genotypes[i] = geno
                                    break
                        else:
                            option == 1
                    if option == 1:
                        # mutate
                        isValid = (False,[])
                        while not isValid[0]:
                            number = randint(1, n)
                            geno = mutate (new_geno [freq_k [number - 1] - 1])
                            isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                            if isValid[0]:
                                genotypes[i] = geno
                                break
                        
        else: # Non of the other cases
            freq = v_freq(sorted(v_result)) # all the vectors and their frequency in the results
            sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
            winners = [] # vectors that survive to the next generation
            #print(sorted_freq)
            for i in range(len(sorted_freq) - 1):
                if i == 0:
                    winners.append(sorted_freq[0][0])
                elif sorted_freq[i][1] == sorted_freq[i-1][1]:
                    #print("en if")
                    winners.append(sorted_freq[i][0])
                else:
                    break
            #print (winners)
            if len(winners) == 1:
                genotypes [0] = genotypes [winners[0] - 1]
                for i in range (1, len(genotypes)):
                    isValid = (False,[])
                    while not isValid[0]:
                        geno = mutate (genotypes[0])
                        isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                        if isValid[0]:
                            genotypes[i] = geno
                            break
            else:
                n = len (winners)
                new_geno = genotypes [::]
                isValid = False
                for i in range (n):
                    genotypes [i] = new_geno [winners [i] - 1]
                for i in range (n, len(genotypes)):
                    option = randint (0,1)
                    if option == 0:
                        v1 = randint(1, n)
                        while True:
                            v2 = randint(1, n)
                            if v2 != v1:
                                break
                        isValid = (False,[])
                        while not isValid[0]:
                            geno = cross (new_geno [winners[v1 - 1] - 1], new_geno [winners[v2 - 1] - 1])
                            isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                            if isValid[0]:
                                genotypes[i] = geno
                                break
                    if option == 1:
                        # mutate
                        isValid = (False,[])
                        while not isValid[0]:
                            number = randint(1, n)
                            geno = mutate (new_geno [winners[number - 1] - 1])
                            isValid = isGenotypeValid(geno, z_function, mjs, limits, restrictions)
                            if isValid[0]:
                                genotypes[i] = geno
                                break                        
                
def mutate (vector):
    #print("mutate")
    rand_index = randint (0, len (vector) - 1)
    temp_l = list (vector)
    if vector [rand_index] == "0":
        temp_l [rand_index] = "1"
    else:
        temp_l [rand_index] = "0"
    new_vector = "".join (temp_l)
    #print(new_vector)
    return new_vector

def cross (v1, v2):
    #print("cross")
    #print(v1); print(v2)
    rand_index = randint (1, len (v1) - 1)
    #print(rand_index)
    new_vector = v1[:rand_index] + v2[rand_index:]
    #print(new_vector)
    return new_vector
    
limits = [] # limits of each variable
mjs = [] # mjs of each variable
genotypes = [] # genotypes generated each generation
result = [] # table of each iteration
v_result = [] # the last column of the table (selected vectors)

for i in range (len(z_function)):
    limits.append(limit(restrictions, i))
    mjs.append(calc_mj (precission_bits, limits[i]))
        
print (mjs)
# for i in range (population): # how many genotypes we want
#     isvalid = (False,[])
#     while not isvalid [0]:
#         geno = generate_genotype(sum(mjs))
#         isvalid = isGenotypeValid (geno, z_function, mjs, limits, restrictions)
#         if isvalid [0]:
#             temp_values = isvalid[1]
#             genotypes.append(geno)
#             result.append([])
#             result[i].append(i + 1)
#             for j in range (len(z_function)):
#                 result[i].append(temp_values[j])
#             break
# #print(result)

# calculateFirstIteration (result, z_function, v_result)
# #print (genotypes)
# for i in range (iterations - 1):
#     evaluateResults(v_result, genotypes, z_function, mjs, limits, restrictions)
#     result = []
#     v_result = []
#     #print (genotypes)
#     for j in range(len(genotypes)):
#         isvalid = isGenotypeValid (genotypes[j], z_function, mjs, limits, restrictions)
#         temp_values = isvalid[1]
#         result.append([])
#         result[j].append(j + 1)
#         for k in range (len(z_function)):
#             result[j].append(temp_values[k])
#     #print(result)
#     calculateFirstIteration (result, z_function, v_result)
# #print (genotypes)
