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

points_file = open('nuvem1.txt', 'r') 

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
    points.append(dt.Point(x,y))

points = random.shuffle(points)

triangle = dt.Triangle(delaunay.envolving_triangle(points_x, points_y))

points = np.append(points, triangle.to_list())

print(triangle.to_list())
figure,axes = plt.subplots(1, 1)

axes.add_artist(triangle.to_plt_artist())

axes.plot()

offset = 500

axes.set_xlim(np.amin(points_x)-offset, np.amax(points_x)+offset)
axes.set_ylim(np.amin(points_y)-offset, np.amax(points_y)+offset)
axes.scatter(points_x, points_y,  marker='.')


plt.show()