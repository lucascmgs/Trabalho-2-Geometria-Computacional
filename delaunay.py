import data_structures as dt
import numpy as np

class TreeNode:
    def __init__(self, given_triangle) -> None:
        self.triangle = given_triangle
        self.children = []
    
    def add_triangles(self, *triangles):
        for t in triangles:
            self.children.append(TreeNode(t))

    def find_triangle_with_point(self, given_point):
        if self.triangle.is_point_inside(given_point):
            if len(self.children) > 0 :
                


def envolving_triangle(points_x, points_y):
    min_x = np.amin(points_x)
    min_y = np.amin(points_y)
    max_x = np.amax(points_x)
    max_y = np.amax(points_y)

    left = dt.Point(min_x-abs(min_x), min_y-abs(min_y))
    right = dt.Point(max_x+abs(max_x), min_y-abs(min_y))
    top = dt.Point((min_x+max_x)/2, max_y+abs(max_y))
    return left, right, top

def triangulate(points, first_triangle):
    triangle_tree_root = TreeNode(first_triangle)
    triangles = []

    for p in points:
        current_node = triangle_tree_root

    