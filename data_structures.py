import math
import matplotlib.pyplot as plt
import numpy as np

class ValuePair:
  def __init__(self, given_x, given_y):
    self.x = given_x
    self.y = given_y
  
  def __str__(self):
    return f"({self.x},{self.y})"

  def __repr__(self):
    return str(self)

  def to_list(self):
    return [self.x, self.y]

  def __eq__(self, o: object) -> bool:
      return self.x == o.x and self.y == o.y
      
  def __ne__(self, o: object) -> bool:
      return self.x != o.x or self.y != o.y
  
  def __hash__(self) -> int:
      return hash(str(self))

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
  


class Edge:
  def __init__(self, first_point, second_point):
    self.q = first_point
    self.r = second_point

  def other_point(self, given_point):
    if self.q == given_point:
      return self.r
    if self.r == given_point:
      return self.q

  def __eq__(self, o: object) -> bool:
    return (self.q == o.r and self.r == o.q) or (self.q == o.q and self.r == o.r)

  def __str__(self) -> str:
      qstr = str(self.q)
      rstr = str(self.r)
      if qstr < rstr:
        return f'{qstr} - {rstr}'
      else:
        return f'{rstr} - {qstr}'

  def __hash__(self) -> int:
      return hash(str(self))


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
   
class Triangle:
   
    def __str__(self):
        point_sum = self.a+self.b+self.c
        sum = point_sum.x + point_sum.y
        return f"T[{self.a}, {self.b}, {self.c}] : {sum}"

    def __repr__(self):
        return str(self)
        

    def __init__(self, given_points) -> None:
        self.points = given_points
        self.a = given_points[0]
        self.b = given_points[1]
        self.c = given_points[2]
        self.tree_node = None
        self.stored_circle = None
        self.init_dict()

    def init_dict(self):
      self.adjacent_triangles_dict = {}
      for p in self.points:
        self.adjacent_triangles_dict[p] = None

    def has_point(self, given_point: Point):
        return self.a == given_point or self.b == given_point or self.c == given_point

    def get_other_points(self, given_point: Point):
        if self.has_point(given_point):
            if given_point == self.a:
                return (self.b, self.c)
            elif given_point == self.b:
                return (self.a, self.c)
            elif given_point == self.c:
                return (self.a, self.b)
        else:
            raise IndexError("The given point is not a part of this triangle")

    def get_other_point(self, first_point, second_point):
        for p in self.points:
          if p != first_point and p != second_point and self.has_point(p):
            return p

    def set_opposing_triangle(self, given_point: Point, given_triangle: "Triangle"):
        (p, q) = self.get_other_points(given_point)

        
        if self.has_point(given_point) and  (given_triangle == None or(given_triangle.has_point(p) and given_triangle.has_point(q))):
            self.adjacent_triangles_dict[given_point] = given_triangle
        else:
            raise IndexError("The given triangle is not adjacent!")

    def get_opposing_triangle(self, given_point: Point):
        
        if self.has_point(given_point):
          if given_point in self.adjacent_triangles_dict:
            return self.adjacent_triangles_dict[given_point]
          else:
            return None
        else:
            raise IndexError("The triangle does not have the specified point!")

    def set_node(self, given_node: "TreeNode"):
        self.tree_node = given_node

    def get_node(self, given_node: "TreeNode"):
        self.tree_node = given_node

    def get_opposing_edge(self, given_point):
      if given_point == self.a:
        return Edge(self.b, self.c)
      if given_point == self.b:
        return Edge(self.c, self.a)
      if given_point == self.c:
        return Edge(self.a, self.b)

    def is_point_inside(self, given_point):
        orient_ab = orient(self.a, self.b, given_point)
        orient_bc = orient(self.b, self.c, given_point)
        orient_ca = orient(self.c, self.a, given_point)

        return ((orient_ab > 0) and (orient_bc > 0) and (orient_ca) > 0)
    
    def is_point_inside_circle(self, given_point):
        circle = self.circle_from_points()
        return circle.is_point_inside(given_point)

    def to_list(self):
        return [self.a.to_list(), self.b.to_list(), self.c.to_list()] 

    def to_plt_artist(self, given_color="green"):
        return plt.Polygon(self.to_list(),color=given_color, fill = None)

    def circle_from_points(self):
        if self.stored_circle == None:
          radius = 0.0
          center = Point(0,0)
          points = self.points
                  
          center = circumcenter(points[0], points[1], points[2])
          radius = (points[0] - center).size()
          self.stored_circle = Circle(center, radius)
        return self.stored_circle
        
class TreeNode:
    def __init__(self, given_triangle) -> None:
        self.triangle = given_triangle
        given_triangle.tree_node = self
        self.children = []
    
    def add_triangles(self, *triangles):
        for t in triangles:
            node = None
            if t.tree_node == None:
              node = TreeNode(t)
              t.set_node(node)
            else:
              node = t.tree_node
            self.children.append(node)

    def find_triangle_with_point(self, given_point):
        print(f'Procurando ponto {given_point}')
        if self.triangle.is_point_inside(given_point):
            if len(self.children) > 0 :
                for node in self.children:
                    test = node.find_triangle_with_point(given_point)
                    if test != None:
                        return test
            else:
                return self
        else:
            return None



def orient(p, q, r):
  return p.x*q.y +p.y*r.x + q.x*r.y -(q.x * p.y + r.x*q.y + r.y*p.x)

def circumcenter(A, B, C):
  denominator = 2*(A.x*(B.y-C.y)+B.x*(C.y-A.y)+C.x*(A.y-B.y))

  A2 = A.x**2+A.y**2
  B2 = B.x**2+B.y**2
  C2 = C.x**2+C.y**2

  Ux = (A2*(B.y-C.y)+B2*(C.y-A.y)+C2*(A.y-B.y))/denominator
  Uy = (A2*(C.x-B.x)+B2*(A.x-C.x)+C2*(B.x-A.x))/denominator

  return Point(Ux, Uy)