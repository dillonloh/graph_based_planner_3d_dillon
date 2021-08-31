#!/usr/bin/env python3
from bresenham import bresenham
from scipy.spatial import Voronoi
import numpy as np
from queue import PriorityQueue
import networkx as nx
from PIL import Image, ImageDraw


def closest_node(graph, current_position):
    '''
    Compute the closest node in the graph to the current position
    '''
    closest_node = None
    dist = 100000
    xyz_position = (current_position[0], current_position[1], current_position[2])
    for p in graph.nodes:
        d = heuristic(xyz_position, p)
        if d < dist:
            closest_node = p
            dist = d
    return closest_node


def create_grid_and_edges(data,e1,e2):
    '''
    Create a grid representation of a 2D configuration space and a Voronoi Graph
    '''
    # given the initial the size of the grid.
    north_size = np.int(np.max(data[:,:]))
    east_size  = np.int(np.max(data[:,:]))

    # Initialize an empty grid
    grid = np.zeros((north_size, east_size))

    # Initialize an empty list for Voronoi points
    points = []

    #graph = Voronoi(points)
    edges = []

    for x in range (data.shape [0] ):
            p1 = ( data[x,0], data[x,1], data[x,2] )
            p2 = ( data[x,3], data[x,4], data[x,5] )
            edges.append((p1, p2))

    #adding elevator lift ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    dist1 = 10000
    dist2 = 10000
    EL1 = (0,0,0)
    EL2 = (0,0,0)
    for x in edges:
        pa = x[0]
        if (pa[0] == 0):
            d1 = heuristic(e1, pa)
            if d1 < dist1:
                EL1 = pa
                dist1 = d1
        pb = x[0]
        if (pb[0] == 20):
            d2 = heuristic(e2, pb)
            if d2 < dist2:
                EL2 = pb
                dist2 = d2
    edges.append((EL1, e1))
    edges.append((e1, e2))
    edges.append((e2, EL2))
    #adding elevator lift ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    return grid, edges

def create_waypoints_edges(data,start,number_list,e1,e2,waypoints_straight):
    '''
    Create a straight egdes between waypoints
    '''
    # Initialize an empty lists
    grid = ()
    points = []
    waypoints_edges = []

    #adding waypoints_edges ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for i in (range(len(number_list))):
        if (number_list[i][0] == e1[0]):
            waypoints_edges.append((number_list[i], e1))
        if (number_list[i][0] == e2[0]):
            waypoints_edges.append((number_list[i], e2))
        if (number_list[i][0] == number_list[i-1][0]):
            waypoints_edges.append((number_list[i], number_list[i-1]))
        waypoints_edges.append((e1, e2))
    #adding waypoints_edges ++++++++++++++++++++++++++++++++++++++++++++++++++++++

    return grid, waypoints_edges

def create_graph(edges, start, goal, data, data1, data2):
    graph = nx.Graph()
    for elem in edges:
        p1 = elem[0]
        p2 = elem[1]
        r1 = elem[0]
        r2 = elem[1]
        dist = heuristic(p1, p2)
        graph.add_edge(p1, p2, weight=dist)

    #Adding HEAT_MAP +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # cells = list(bresenham(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])))
        # num=0
        # for i in cells:
        #     #Inputing the initial heatmap
        #     heatmap = Image.open ('./images/heatmap_NIC6F.png')
        #     rgb_heatmap = heatmap.convert('RGB')
        #     r,g,b = (rgb_heatmap.getpixel ( (i) ))
        #     ave_rgb = (r+g+b)/(255*3)
        #     num += 1
        #     dist += (dist*ave_rgb)/num
        # graph.add_edge(p1, p2, weight=dist)
    #Adding HEAT_MAP +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #Adding manual BEHAVIOR +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # for x in range ( data1.shape [0] ):
    #     l1 = ( data1[x,0], data1[x,1], data1[x,2] )
    #     l2 = ( data1[x,3], data1[x,4], data1[x,5] )
    #     dist = heuristic(l1, l2)
    #     if ( start[1] < goal[1]):
    #         dist = dist*1.0
    #     else:
    #         dist = dist*1.5
    #     graph.add_edge(l1, l2, weight=dist)
    # for x in range ( data2.shape [0] ):
    #     r1 = ( data2[x,0], data2[x,1], data2[x,2] )
    #     r2 = ( data2[x,3], data2[x,4], data2[x,5] )
    #     dist = heuristic(r1, r2)
    #     if ( start[1] < goal[1]):
    #         dist = dist*1.5
    #     else:
    #         dist = dist*1.0
    #     graph.add_edge(r1, r2, weight=dist)
    #Adding manual BEHAVIOR +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #Adding BEHAVIOR +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # distA = heuristic(p1, p2)*0.6
        # distB = heuristic(r1, r2)*0.4
        # graph.add_edge(p2, p1, weight=distA)
        # if ( start[1] < goal[1]):
        #     A = area_triangle(r1,r2,start)
        #     distB = (distB/A)
        # else:
        #     distB = distA
        # graph.add_edge(r1, r2, weight=distB)
    #Adding BEHAVIOR +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    return graph


def heuristic(n1, n2):
    return ( (n1[0]-n2[0])**2 +(n1[1]-n2[1])**2 +(n1[2]-n2[2])**2 )**0.5

def area_triangle(a, b, c):
    a = heuristic(a,c)
    b = heuristic(b,c)
    c = heuristic(a,b)
    s = ( a + b + c)/2
    return ((s*(s-a)*(s-b)*(s-c)) ** 0.5)

def a_star_graph(graph, start, goal, h):
    '''
    A* working with NetworkX graphs
    '''
    path = []
    path_cost = 0
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set(start)

    branch = {}
    found = False

    while not queue.empty():
        item = queue.get()
        current_node = item[1]
        if current_node == start:
            current_cost = 0.0
        else:
            current_cost = branch[current_node][0]

        if current_node == goal:
            print('Found a path.')
            found = True
            break
        else:
            for next_node in graph[current_node]:
                cost = graph.edges[current_node, next_node]['weight']
                branch_cost = current_cost + cost
                queue_cost = branch_cost + h(next_node, goal)

                if next_node not in visited:
                    visited.add(next_node)
                    branch[next_node] = (branch_cost, current_node)
                    queue.put((queue_cost, next_node))

    if found:
        # retrace steps
        n = goal
        path_cost = branch[n][0]
        path.append(goal)
        while branch[n][1] != start:
            path.append(branch[n][1])
            n = branch[n][1]
        path.append(branch[n][1])
    else:
        print('**********************')
        print('Failed to find a path!')
        print('**********************') 
    return path[::-1], path_cost


def a_star_graph_WP(graph, start, number_list, h):
    '''
    A* working with NetworkX graphs
    '''
    path = []
    path_cost = 0
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set(start)

    branch = {}
    found = False

    while not queue.empty():
        item = queue.get()
        current_node = item[1]
        if current_node == start:
            current_cost = 0.0
        else:
            current_cost = branch[current_node][0]

        if current_node == number_list:
            print('Found a path_WP.')
            found = True
            break
        else:
            for next_node in graph[current_node]:
                cost = graph.edges[current_node, next_node]['weight']
                branch_cost = current_cost + cost
                queue_cost = branch_cost + h(next_node, number_list)

                if next_node not in visited:
                    visited.add(next_node)
                    branch[next_node] = (branch_cost, current_node)
                    queue.put((queue_cost, next_node))

    if found:
        # retrace steps
        n = number_list
        path_cost = branch[n][0]
        path.append(number_list)
        while branch[n][1] != start:
            path.append(branch[n][1])
            n = branch[n][1]
        path.append(branch[n][1])
    else:
        print('**********************')
        print('Failed to find a path_WP!')
        print('**********************') 
    return path[::-1], path_cost