from math import log
from math import ceil
from random import randint

r_coefficients = [[2, 4, "le", 125], [3, 5, "le", 100], [1, 0, "ge", 15], [0, 1, "ge", 0]]
precission_bits = 2

def limit (n_variables, restrictions, varpos):
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

def calculate_var_value (var_bin, upper_limit, lower_limit, mj):
    return lower_limit  + var_bin * ((upper_limit - lower_limit)/ ((2 ** mj) - 1))

#print ("x lim: " + str(limit (2, r_coefficients, 0)))
#print ("y lim: " + str (limit (2, r_coefficients, 1)))

#print ("x mj: " + str (calc_mj(precission_bits, limit (2, r_coefficients, 0))))
#print ("y mj: " + str (calc_mj(precission_bits, limit (2, r_coefficients, 1))))
    
#print (int(generate_genotype (10)))
#print (str(int("010001010111", 2)))
#print (str ((47.5 / 4096)))
print (str (calculate_var_value (int("010001010111", 2), 62.5, 15, 12)))

