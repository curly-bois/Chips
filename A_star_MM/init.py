from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv
import re
import os
import heapq
import itertools
from point import Point
from netlists import *
from grids import *


def make_grid(grid):

    points = get_grid(grid)

    grid = {}
    num = 1
    for point in points:
        x = int(point[0])
        y = int(point[1])

        grid[x, y] = num
        num += 1

    return grid


def get_connections(list):

    netlist = get_netlist(list)
    connections = []

    # add 1 to make the connections valid
    for tup in netlist:
        connections.append((tup[0] + 1, tup[1] + 1))

    return connections


def make_matrix(grid):

    z = 7
    tuplist = []

    for tup in grid:
        tuplist.append(tup)
    x = max(tuplist, key=itemgetter(0))[0] + 1
    y = max(tuplist, key=itemgetter(1))[1] + 1
    matrix = [[[0 for x in range(x)]
               for y in range(y)]
              for z in range(z)]

    for i in range(z):
        for j in range(y):
            for k in range(x):
                # Point in 3d matrix is a gate
                if tuple([k, j]) in tuplist and i == 0:
                    matrix[i][j][k] = Point(
                        (k, j, i), "gate", [], 0, grid[k, j])
                # Point is empty
                else:
                    matrix[i][j][k] = Point((k, j, i), "empty", [], 0)

    gates = []
    # Initialize neighbours
    for i in range(z):
        for j in range(y):
            for k in range(x):

                neighbours = []

                # Northern neighbour
                if j + 1 < y:
                    neighbours.append(matrix[i][j + 1][k])

                # Eastern neighbour
                if k + 1 < x:
                    neighbours.append(matrix[i][j][k + 1])

                # Southern neighbour
                if j - 1 >= 0:
                    neighbours.append(matrix[i][j - 1][k])

                # Western neighbour
                if k - 1 >= 0:
                    neighbours.append(matrix[i][j][k - 1])

                # Upper neighbour
                if i + 1 < z:
                    neighbours.append(matrix[i + 1][j][k])

                # Down neighbour
                if i - 1 >= 0:
                    neighbours.append(matrix[i - 1][j][k])

                matrix[i][j][k].set_neighbours(neighbours)
                if matrix[i][j][k].attribute == "gate":
                    gates.append(matrix[i][j][k].location)

    return matrix


def make_conlist(connections, matrix):

    locations = []
    coordinates = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                if matrix[i][j][k].id > 0:
                    coordinates[matrix[i][j][k].id] = matrix[i][j][k]

    for connection in connections:
        # connection[0] += 1
        # connection[1] += 1
        locations.append(
            (coordinates[connection[0]], coordinates[connection[1]]))

    return locations
