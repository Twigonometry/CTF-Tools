import cmath

"""
In true celebration of polynomial majesty, here are some sets of coefficients. I reckon if you find their sum of roots, there may be something for you.
"""

coeffs = [
    [832, -112, 1],
    [888, -119, 1],
    [721, -110, 1],
    [294, -101, 1],
    [736, -100, 1],
    [812, -123, 1],
    [637, -98, 1],
    [147, -52, 1],
    [644, -99, 1],
    [882, -107, 1],
    [534, -95, 1],
    [115, -116, 1],
    [47, -48, 1],
    [774, -95, 1],
    [303, -104, 1],
    [138, -49, 1],
    [300, -103, 1],
    [855, -104, 1],
    [94, -95, 1],
    [336, -115, 1],
    [288, -99, 1],
    [495, -104, 1],
    [47, -48, 1],
    [351, -48, 1],
    [107, -108, 1],
    [364, -95, 1],
    [392, -57, 1],
    [320, -48, 1],
    [336, -55, 1],
    [552, -98, 1],
    [360, -49, 1],
    [220, -49, 1],
    [388, -101, 1],
    [329, -54, 1],
    [366, -125, 1],
]

sols = []

for cs in coeffs:
    d = (cs[1]**2) - (4*cs[0]*cs[2])
    sol1 = (-cs[1] - cmath.sqrt(d))/(2*cs[0])
    sol2 = (-cs[1] + cmath.sqrt(d))/(2*cs[0])
    sols.append([sol1, sol2, sol1 + sol2])

print(sols)

sums = [sol[2] for sol in sols]

print(sums)

# chars = ''.join([chr(sum.real) for sum in sums])

reals = [sum.real for sum in sums]
print(sum(reals)) #11.42515715085705