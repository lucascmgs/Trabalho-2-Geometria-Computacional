import data_structures as dt
import numpy as np



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
    triangle_tree_root = dt.TreeNode(first_triangle)
    first_triangle.set_node(triangle_tree_root)

    print (points)
    triangulation = set()
    triangulation.add(first_triangle)
    
    cont = 0
    for p in points:
        cont = cont+1
        print(f"iteração {cont}")
        first_node = triangle_tree_root
        target_node = first_node.find_triangle_with_point(p)
        if target_node == None:
            continue
        target_triangle = target_node.triangle
        triangles_to_process = []
        marked_triangles = set()

        #Armazena as arestas do polígono demarcado e as associa com o triângulo removido ao qual elas pertencem,
        #bem como o vizinho desse triângulo que está fora do polígono
        opposing_edge_with_triangles = {}

        triangles_to_process.append(target_triangle)
        marked_triangles.add(target_triangle)

        while(len(triangles_to_process) > 0):
            current_triangle = triangles_to_process.pop()
            
            for vertex, neighboor in current_triangle.adjacent_triangles_dict.items():
                edge = current_triangle.get_opposing_edge(vertex)

                if neighboor == None:
                    opposing_edge_with_triangles[edge] = (current_triangle,None)
                    continue
                if neighboor.is_point_inside_circle(p):
                    if(neighboor not in marked_triangles):
                        triangles_to_process.append(neighboor)
                        marked_triangles.add(neighboor)
                else:
                    opposing_edge_with_triangles[edge] = (current_triangle, neighboor)
       

        for t in marked_triangles:
            triangulation.remove(t)

        #Dicionário que mapeia pontos já visitados às arestas correspondentes
        visited_points = {}
        edges_to_triangles = {}

        #Insere novo triangulo na triangulação e ajusta vizinhanças
        for edge, (father_triangle, neighboor) in opposing_edge_with_triangles.items():
            q = edge.q
            r = edge.r
            
            new_triangle = None
            if dt.orient(p, q, r) > 0:
                new_triangle = dt.Triangle([p, q, r])
            else:
                new_triangle = dt.Triangle([p, r, q])
            target_node.add_triangles(new_triangle)
            father_triangle.tree_node.add_triangles(new_triangle)

            new_triangle.set_opposing_triangle(p, neighboor)
            
            if neighboor != None:
                neighboor.set_opposing_triangle(neighboor.get_other_point(q, r), new_triangle)

            #Indicamos que essa aresta pertence a este triângulo
            edges_to_triangles[edge] = new_triangle

            #Adicionamos triangulo à triangulação
            triangulation.add(new_triangle)

            for edge_point in [q, r]: 
                #Se já visitamos este ponto durante a costura, ele pertence a uma aresta compartilhada por outro triângulo, que é um vizinho a ser adicionado
                if edge_point in visited_points:
                    common_edge = visited_points[edge_point]
                    neighboor = edges_to_triangles[common_edge]
                    #Adicionamos o triângulo já criado como vizinho do novo triângulo
                    new_triangle.set_opposing_triangle(edge.other_point(edge_point), neighboor)
                    #Adicionamos o novo triângulo como vizinho do triângulo já encontrado anteriormente
                    neighboor.set_opposing_triangle(common_edge.other_point(edge_point), new_triangle)
                #Do contrário, marcamos o ponto como visitado e damos a aresta correspondente
                else:
                    visited_points[edge_point] = edge

                
    return triangulation
                

            


    