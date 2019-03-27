from math import log
from math import ceil
from random import randint
from random import uniform
from tabulate import tabulate

iterations = 3
precission_bits = 2
population = 10
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

def getHeaders (n):
    my_headers = ["Vector"]
    for i in range (n):
        my_headers.append ("X"+str(i))
    my_headers.append("Z"); my_headers.append("%Z"); my_headers.append("%Z acc");
    my_headers.append("rand[0,1]"); my_headers.append("Vector *")
    return my_headers

def calculateFirstIteration (result, z_function):
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
    
    print(tabulate(result, getHeaders(m)))

#001100
def mutate (vector):
#    rand_index = randint (0, len(vector) - 1)
    rand_index = 0
    if rand_index == 0:
        if vector [0] == "0":
            new_vector = "1" + vector[1:]
        else:
            new_vector = "0" + vector[1:]
    
    print(new_vector)
    return vector




limits = [] # limits of each variable
mjs = [] # mjs of each variable
genotypes = [] # genotypes generated each generation
result = []

for i in range (len(z_function)):
    limits.append(limit(restrictions, i))
    #print("* Limits of X" + str (i) +" are: " + str(limits[i]))
    mjs.append(calc_mj (precission_bits, limits[i]))
    #print("* Mj of X" + str (i) +" is: " + str(mjs[i]) + "\n")
    
    
for i in range (population): # how many genotypes we want
    isvalid = False
    while not isvalid:
        temp_values = []
        geno = generate_genotype(sum(mjs))
        #print(str (i + 1) +".- Genotype generated: " + geno)

        for j in range (len (z_function)):
            if j == 0:
                fenotype = geno[0:mjs[j]]      
            else:
                fenotype = geno[mjs[j - 1]: mjs[j - 1] + mjs[j]]            
            
            #print ("** Fenotype " + str(j) + ": " + fenotype + " len: " + str(len(fenotype)) + " decimal value: " + str (int(fenotype, 2)))
            
            temp_values.append(var_value(int(fenotype, 2), limits[j][1], limits[j][0], mjs[j]))
            
        #print ("** Values for genotype: " + str(temp_values))
        isvalid = areValuesValid(temp_values, restrictions)
        #print ("** Is this genotype valid?: " + str (isvalid) + "\n")
        if isvalid:
            genotypes.append(geno)
            result.append([])
            result[i].append(i + 1)
            for j in range (len(z_function)):
                result[i].append(temp_values[j])
            break

#calculateFirstIteration(result, z_function)
mutate ("001100")