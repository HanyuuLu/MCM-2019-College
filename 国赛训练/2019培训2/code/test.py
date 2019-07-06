from sympy import *
import node

sysInfo = node.SysInfo()
calc = list()
var = list()
for i in range(10):
    var.append(symbols('var_%d' % i))
calc.append(var[0]+var[1])
print(var)
s = 0
a = 5
for i in var:
    s += i
s += sysInfo.WaterDeepth
calc.append(s)
print(calc)
