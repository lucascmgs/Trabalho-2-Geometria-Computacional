import data_structures as dt
from typing import Union

lista = {}

a = dt.Point(0, 0)
b = dt.Point(1, 2323)
c = dt.Point(3, 23232)

tri = dt.Triangle([a, b, c])

p = dt.Point(2, 3)

lista[p] = tri

print(tri in lista)

class Tlup :
    def __init__(self, given_a) -> None:
        self.a = given_a


conjunto = set()
conjunto.add(tri)
conjunto.remove(tri)

print (conjunto)

tlup = Tlup(2)
tlup.b = 3
print(tlup.b)