import data_structures as dt
import matplotlib.pyplot as plt
import numpy as np
import random
import delaunay

def generate_random_values(numero_amostras, espalhamento):
    values = []
    for i in range(numero_amostras):
        value = random.random()*espalhamento
        values.append([value])
    return values

points_file = open('nuvem2.txt', 'r') 

lines = points_file.readlines()

points_x = []
points_y = []
points = []

for line in lines :
    elements = line.split('  ')
    elements[1] = elements[1].strip()
    x = float(elements[0])
    y = float(elements[1])
    points_x.append([x])
    points_y.append([y])
    point = dt.Point(x,y)
    points.append(point)

#random.shuffle(points)

first_triangle = dt.Triangle(delaunay.envolving_triangle(points_x, points_y))

# points.append(first_triangle.a)
# points.append(first_triangle.b)
# points.append(first_triangle.c)


figure,axes = plt.subplots(1, 1)

triangulation = delaunay.triangulate(points, first_triangle)

for t in triangulation:
    if t.has_point(first_triangle.a) or t.has_point(first_triangle.b) or t.has_point(first_triangle.c) :
        continue
    axes.add_artist(t.to_plt_artist())

axes.plot()

offset = 500

axes.set_xlim(np.amin(points_x)-offset, np.amax(points_x)+offset)
axes.set_ylim(np.amin(points_y)-offset, np.amax(points_y)+offset)
axes.scatter(points_x, points_y,  marker='.')


plt.show()