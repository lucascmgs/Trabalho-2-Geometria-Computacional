import math
import matplotlib.pyplot as plt

class ValuePair:
  def __init__(self, given_x, given_y):
    self.x = given_x
    self.y = given_y
  
  def __str__(self):
    return f"({self.x},{self.y})"

  def to_list(self):
    return [self.x, self.y]

  def __eq__(self, o: object) -> bool:
      return self.x == o.x and self.y == o.y
      
  def __ne__(self, o: object) -> bool:
      return self.x != o.x or self.y != o.y

class Vec(ValuePair):
  def size(self):
    return math.sqrt(self.x**2+self.y**2)
  def dot(self, other_vector):
    return self.x * other_vector.x + self.y * other_vector.y

  def __mul__(self, scalar:float):
    return Vec(self.x*scalar, self.y*scalar)

  def __truediv__(self, scalar:float):
    return Vec(self.x/scalar, self.y/scalar)

  def normalized(self):
    current_size = self.size()
    return self/current_size

  def angle(self, other_vector: object):
    pass
  
  def pseudoangle(self, other_vector):
    return 1 - (self/self.size()).dot(other_vector/other_vector.size())


class Point(ValuePair):
  def __add__(self, other_point):
    return Point(self.x + other_point.x, self.y + other_point.y)

  def __sub__(self, other_point):
    return Vec(self.x - other_point.x, self.y - other_point.y)

  def __truediv__(self, scalar:float):
    return Point(self.x/scalar, self.y/scalar)


class Circle:
  def __init__(self, given_center:Point, given_radius:float):
    self.center = given_center
    self.radius = given_radius

  def __str__(self):
    return f"(Center: {self.center}, Radius: {self.radius})"

  def is_point_inside(self, given_point):
    distance_to_point = (given_point-self.center).size()
    if distance_to_point <= self.radius:
      return True
    else:
      return False
  


class HalfEdge:
    def __init__(self, given_vertex: Point) -> None:
        self.vertex = given_vertex

    def __init__(self, given_vertex: Point, given_next: "HalfEdge") -> None:
        self.vertex = given_vertex
        self.next = given_next

    def set_next(self, given_next: "HalfEdge"):
        self.next = given_next

    def set_edge(self, given_edge: "Edge"):
        self.edge = given_edge

class Edge:
    def __init__(self, given_first_he: HalfEdge, given_second_he: HalfEdge) -> None:
        self.first_vertex = given_first_vertex
        self.second_vertex = given_second_vertex
        
class Triangle:
    def __init__(self, a, b, c) -> None:
        self.points = [a,b,c]
        self.a = a
        self.b = b
        self.c = c
    def __init__(self, points) -> None:
        self.points = points
        self.a = points[0]
        self.b = points[1]
        self.c = points[2]
        
    def is_point_inside(self, given_point):
        orient_ab = orient(self.a, self.b, given_point)
        orient_bc = orient(self.b, self.c, given_point)
        orient_ca = orient(self.c, self.a, given_point)

        return ((orient_ab > 0) and (orient_bc > 0) and (orient_ca) > 0)

    def to_list(self):
        return [self.a.to_list(), self.b.to_list(), self.c.to_list()] 

    def to_plt_artist(self, given_color="green"):

      return plt.Polygon(self.to_list(),color=given_color, fill = None)


def orient(p, q, r):
  return p.x*q.y +p.y*r.x + q.x*r.y -(q.x * p.y + r.x*q.y + r.y*p.x)