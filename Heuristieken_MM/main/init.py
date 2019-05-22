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
    ## Hard coded
    z = 7
    tuplist = []

    for tup in grid:
        tuplist.append(tup)
    x = max(tuplist, key=itemgetter(0))[0] + 2
    y = max(tuplist, key=itemgetter(1))[1] + 2

    ## Je kan deze matrix en de hier na komende nested for loops in een 'regel'
    ## Schrijven, door ze een functie te geven die de if else aanpakt.
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
                    ## JE kan ook deze waardes van te voren als leeg zetten
                    ## In de class, dan hoef je ze ook niet hier als random
                    ## waardes neer te zetten
                    matrix[i][j][k] = Point((k, j, i), "empty", [], 0)

    gates = []
    # Initialize neighbours
    ## Dit had ik al getyped, had veel kunnen schelen
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

    ## Moet je hier een aparte variable voor maken?
    for neighbour in matrix[i][j][k].get_neighbours():
        if neighbour.get_attribute() == "gate" and matrix[i][j][k].get_attribute() != "gate":
            matrix[i][j][k].next_to_gate = True

    return matrix


def make_conlist(connections, matrix):
    setlist = []
    locations = []
    coordinates = {}

    ## Je loopt hier door de lengte van de matrix of ze vervolgens als index
    ## Te gebruiken, je kan ook een lijst maken van de matrix en hier over loopen
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

def make_order(sets):

    horizontal = {}
    vertical = {}
    diagonalup = {}
    diagonaldown = {}
    horlist = []
    verlist = []
    diadownlist = []
    diauplist = []


    for set in sets:
        if set.direction == "horizontal":
            horizontal[set] = set.distance
        elif set.direction == "vertical":
            vertical[set] = set.distance
        elif set.direction == "diagonal-down":
            diagonaldown[set] = set.distance
        elif set.direction == "diagonal-up":
            diagonalup[set] = set.distance




    temp = sorted(diagonaldown.items(), key=operator.itemgetter(1))
    for i in temp:
        diadownlist.append(i[0])
    temp = sorted(diagonalup.items(), key=operator.itemgetter(1))
    for i in temp:
        diauplist.append(i[0])
    temp = sorted(horizontal.items(), key=operator.itemgetter(1))
    for i in temp:
        horlist.append(i[0])
    temp = sorted(vertical.items(), key=operator.itemgetter(1))
    for i in temp:
        verlist.append(i[0])


    complete = list(diauplist+diadownlist+verlist+horlist)

    return complete
