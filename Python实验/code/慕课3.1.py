from math import *
# pi = 3.1415926

r = input()
r = int(r)
b = (r*sin(36/360*2*pi))/sin(126/360*2*pi)

print('{0:.2f}'.format(b))
