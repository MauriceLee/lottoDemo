from sympy import integrate, exp, pi, sqrt, symbols, N
import json

x = symbols('x')


def normalStandard(a, b):
    return integrate((1/sqrt(2*pi))*exp(-x**2/2), (x, a, b))


normalList = {}
tempList = {}

for item in range(360):
    normalProb = round(N(normalStandard(0, item*0.01), 4), 4)
    tempList[round((item % 10)*0.01, 2)] = normalProb
    if (item % 10 == 9):
        index = round((item-9)*0.01, 1)
        tempList["z"] = index
        normalList[index] = tempList
        tempList = {}

with open("./public/normal_table.json", 'w') as f:
    json.dump(normalList, f)
