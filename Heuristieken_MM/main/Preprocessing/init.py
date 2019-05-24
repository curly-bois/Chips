from operator import itemgetter
import numpy as np
import re
import os
import heapq
import operator
import itertools
from Classes.point import Point
from Classes.set import Set
from options.netlists import *
from options.grids import *

# function for making the grid according to its coordinates
def make_grid(grid):

    # get gates on the grid from options/grids
    points = get_grid(grid)


    grid = {}

    # give the gate the appointing number
    for i, point in enumerate(points):
        x = int(point[0])
        y = int(point[1])

        grid[x, y] = i + 1

    return grid


def get_connections(list):

    # get the netlist of gates to connect.
    netlist = get_netlist(list)
    connections = []

    # add 1 to make the connections valid (difference of 1 in the netlist and on the grid)
    for tup in netlist:
        connections.append((tup[0] + 1, tup[1] + 1))

    return connections


def make_matrix(grid,netlist):

    # define the height of the matrix
    z = 7
    tuplist = []

    # get the highest x and y value to make a matrix that is the  right size
    for tup in grid:
        tuplist.append(tup)
    x = max(tuplist, key=itemgetter(0))[0] + 2
    y = max(tuplist, key=itemgetter(1))[1] + 2

    # make the 3d matrix
    matrix = [[[0 for x in range(x)]
               for y in range(y)]
              for z in range(z)]

    # if the coordinates match a gate make it a gate in the point class
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
                matrix[i][j][k].set_appearence(netlist)
                if matrix[i][j][k].attribute == "gate":
                    gates.append(matrix[i][j][k].location)

    ## Moet je hier een aparte variable voor maken?
    for neighbour in matrix[i][j][k].get_neighbours():
        if neighbour.get_attribute() == "gate" and matrix[i][j][k].get_attribute() != "gate":
            matrix[i][j][k].next_to_gate = True

    return matrix


def make_conlist(connections, matrix):
    setlist = []
    locations = []
    coordinates = {}

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                if matrix[i][j][k].id > 0:
                    coordinates[matrix[i][j][k].id] = matrix[i][j][k]

    for connection in connections:
        locations.append(
            (coordinates[connection[0]], coordinates[connection[1]]))
        setlist.append(Set(coordinates[connection[0]], coordinates[connection[1]]))

    return setlist
