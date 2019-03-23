# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 22:22:51 2019

@author: elpat
"""
variables = 0
restrictions = 0
while True:
    variables = int(input ("How many variables are in your problem? (max: 4) "))
    if variables > 0 and variables <= 4:
        break
while True:
    restrictions = int(input("How many restrictions are in your problem? (max: 5) "))
    if restrictions > 0 and restrictions <= 5:
        break

z_coefficients = [] # list containing the coefficients of the Z function
r_coefficients = [] # list containing the lists of coeficcients of each restriction

print("Please insert the coefficients of your variables in Z:")
for i in range (variables):
    coef = int(input("Coefficient for x" + str(i) + ": "))
    z_coefficients.append(coef)
    
print("Please insert the coefficients of your variables for each restriction")
for i in range (restrictions):
    print("Restriction " + str (i))
    r_coefficients.append([])
    for j in range (variables):
        coef = int(input("Coefficient for x" + str(j) + ": "))
        r_coefficients[i].append(coef)
