#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib._png import read_png
import matplotlib.image as mpimg
from PIL import Image, ImageDraw
import networkx as nx
import sys,os,time

from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from lib.voronoi_utils import a_star_graph, a_star_graph_WP, closest_node, create_grid_and_edges, create_waypoints_edges, create_graph, heuristic

def plotGridEdges(grid, edges):
    plt.imshow(grid, origin='lower', cmap='Greys')

    for e in edges:
        p1 = e[0]
        p2 = e[1]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'b-')
    plt.show()

def plotVoronoiPath(grid, edges, path, start, goal, start_graph, goal_graph):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    map1 = mpimg.imread('./images/chinokyoten1f.png')
    map2 = mpimg.imread('./images/chinokyoten2f.png')
    map3 = mpimg.imread('./images/chinokyoten3f.png')

    ax.set_xlim(0, map1.shape[0])
    ax.set_ylim(0, map1.shape[1])
    ax.set_zlim(0, 20)
    x, y = np.ogrid[0:map1.shape[0], 0:map1.shape[1]] # Creates two arrays of coordinates for a meshgrid https://numpy.org/doc/stable/reference/generated/numpy.ogrid.html
    ax.plot_surface(x, y, np.atleast_2d(0), rstride=10, cstride=10, shade=False) # np.atleast_2d makes its input into at least a 2d array e.g. 0 -> [[0]]
    ax.plot_surface(x, y, np.atleast_2d(10), rstride=10, cstride=10, shade=False)
    ax.plot_surface(x, y, np.atleast_2d(20), rstride=10, cstride=10, shade=False)

    for e in edges:
        p1 = e[0]
        p2 = e[1]
        #voronoi_edges is not necessary to be shown
        #plt.plot([p1[2], p2[2]], [p1[1], p2[1]], [p1[0], p2[0]], 'b-')

    plt.plot([start[2], start_graph[2]], [start[1], start_graph[1]], [start[0], start_graph[0]], 'r-')

    if (waypoints != 1):
        for i in range(len(path)-1):
            p1 = path[i]
            p2 = path[i+1]
            plt.plot([p1[2], p2[2]], [p1[1], p2[1]], [p1[0], p2[0]], 'r-')
        plt.plot([goal[2], goal_graph[2]], [goal[1], goal_graph[1]], [goal[0], goal_graph[0]], 'r-')
    elif (waypoints == 1):
        for x in range(len(path)-1):
            p1 = path[x]
            p2 = path[x+1]
            plt.plot([p1[2], p2[2]], [p1[1], p2[1]], [p1[0], p2[0]], 'b-')
        plt.plot([w1[2], w1_graph[2]], [w1[1], w1_graph[1]], [w1[0], w1_graph[0]], 'b-')

    for i in (range(len(number_list))):
        ax.plot([number_list[i][2]], [number_list[i][1]], [number_list[i][0]], 'ko', markersize=3)
    ax.plot([start[2]], [start[1]], [start[0]], 'go', markersize=3)
    ax.plot([goal[2]], [goal[1]], [goal[0]], 'ro', markersize=3)
    ax.plot([e1[2]], [e1[1]], [e1[0]], 'bo', markersize=3)
    ax.plot([e2[2]], [e2[1]], [e2[0]], 'bo', markersize=3)

    ax.set_xlabel('EAST', fontsize=20)
    ax.set_ylabel('NORTH', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)
    plt.show()


if __name__ == "__main__":
    t0 = time.perf_counter()
    filename = 'data/NIC6F_voronoi_data.txt'
    data = np.loadtxt(filename, delimiter=' ', dtype='float', skiprows=0)
    # Split input data by row and then on spaces
    rows = [ line.strip().split(' ') for line in filename.split('\n') ]
    cols = zip(*rows)

    filename1 = 'data/NIC6F_L1.txt'
    data1 = np.loadtxt(filename1, delimiter=' ', dtype='float', skiprows=0)
    # Split input data by row and then on spaces
    rows1 = [ line.strip().split(' ') for line in filename1.split('\n') ]

    filename2 = 'data/NIC6F_R1.txt'
    data2 = np.loadtxt(filename2, delimiter=' ', dtype='float', skiprows=0)
    # Split input data by row and then on spaces
    rows2 = [ line.strip().split(' ') for line in filename2.split('\n') ]

    #NIC6F_elevator
    e1 = (0,947,567)
    e2 = (20,947,567)

    #NIC6F
    start = (0,740, 680)
    goal = (20,900, 735)

    #NIC6F_waypoints
    waypoints = 0
    waypoints_straight = 0

    w_start = start
    w1 = (0,740,645)
    w2 = (0,870,540)
    w3 = (20,900,570)
    w4 = (20,925,620)
    w_final = goal
    number_list = [w_start, w1, w2, w3, w4, w_final]

    if (waypoints == 1 and waypoints_straight == 1):
        grid, waypoints_edges = create_waypoints_edges(data,start,number_list,e1,e2,waypoints_straight)
        graph = create_graph(waypoints_edges, start, goal, data, data1, data2)
    elif (waypoints != 1 or waypoints_straight != 1):
        grid, edges = create_grid_and_edges(data,e1,e2)
        graph = create_graph(edges, start, goal, data, data1, data2)

    start_graph = closest_node(graph, start)
    goal_graph = closest_node(graph, goal)
    w1_graph = closest_node(graph, w1)
    w2_graph = closest_node(graph, w2)
    w3_graph = closest_node(graph, w3)
    w4_graph = closest_node(graph, w4)
    w_final_graph = closest_node(graph, w_final)


    if (waypoints == 1):
        path_WP = []
        for i in (range(len(number_list)-1)):
            w_graph1 = closest_node(graph, number_list[i])
            w_graph2 = closest_node(graph, number_list[i+1])
            path, cost = a_star_graph_WP(graph, w_graph1, w_graph2, heuristic)
            path_WP.extend(path)
        if (waypoints_straight == 1):
            plotVoronoiPath(grid, waypoints_edges, path_WP, start, goal, start_graph, goal_graph)

        elif (waypoints_straight != 1):
            plotVoronoiPath(grid, edges, path_WP, start, goal, start_graph, goal_graph)


    elif (waypoints != 1):
        path, cost = a_star_graph(graph, start_graph, goal_graph, heuristic)
        plotVoronoiPath(grid, edges, path, start, goal, start_graph, goal_graph)

    t1 = time.perf_counter()
    total = t1-t0
    print('Compu. time =', total)
    # number_list[-1] = goal
    # number_list[-2] = (20,925,620)
    # number_list[-3] = (20,900,570)
    # number_list[-4] = (0,870,540)
    # number_list[-5] = (0,740,645)
    # number_list[ 0] = start
