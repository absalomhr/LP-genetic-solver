from math import log
from math import ceil
from random import randint

z_function = [1, 1]
restrictions = [[2, 4, "le", 125], [3, 5, "le", 100], [1, 0, "ge", 15], [0, 1, "ge", 0]]
precission_bits = 2

def limit (restrictions, varpos):
    limits = []
    for i in range(len(restrictions)):
        var_coeff = restrictions[i][varpos]
        eq_res = restrictions[i][-1]
        if (var_coeff != 0):
            limits.append (eq_res / var_coeff)
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
    #print (str(constant))
    return lower_limit  + (var_bin * (constant))

def areValuesValid (values, restrictions, n_variables): # Is the value of the variable valid for all restrictions
    for i in range(len(restrictions)):
        res = 0
        current = 0
        print("*** Restriction " + str (i + 1))
        for j in range(n_variables):
            current = values [j] * restrictions [i][j]
            res += current
            print ("**** evaluation of X" + str(j) + ": " + str(restrictions [i][j]) + "*" + str(values [j]) + " = " + str (current))
        if restrictions[i][n_variables] == "le":
            print ("***** Is " + str (res) + " <= " + str(restrictions[i][-1]))
            if not (res <= restrictions[i][-1]):
                return False
        elif restrictions[i][n_variables] == "ge":
            print ("***** Is " + str (res) + " >= " + str(restrictions[i][-1]))
            if not (res >= restrictions[i][-1]):
                return False
    return True

limits = [] # limits of each variable
mjs = [] # mjs of each variable
genotypes = [] # genotypes generated each generation
values = [] # the values of each fenotype (variable) of each genotype
for i in range (len(z_function)):
    limits.append(limit(restrictions, i))
    print("* Limits of X" + str (i) +" are: " + str(limits[i]))
    mjs.append(calc_mj (precission_bits, limits[i]))
    print("* Mj of X" + str (i) +" is: " + str(mjs[i]) + "\n")
for i in range (10): # how many genotypes we want
    genotypes.append(generate_genotype(sum(mjs)))
    print(str (i + 1) +".- Genotype generated: " + genotypes[i])
    values.append([])
    for j in range (len (z_function)):
        if j == 0:
            fenotype = genotypes[i][0:mjs[j]]      
        else:
            fenotype = genotypes[i][mjs[j - 1]: mjs[j - 1] + mjs[j]]            
        print ("** Fenotype " + str(j) + ": " + fenotype + " len: " + str(len(fenotype)) + " decimal value: " + str (int(fenotype, 2)))
        values[i].append(var_value(int(fenotype, 2), limits[j][1], limits[j][0], mjs[j]))
    print ("** Values for genotype: " + str(values [i]))
    print ("** Is this genotype valid?: " + str (areValuesValid(values[i], restrictions, len(z_function))) + "\n")
        