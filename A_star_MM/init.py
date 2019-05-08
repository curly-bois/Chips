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
from set import Set


def get_grid():

    # make a dict of all the points and their location
    points = []

    txt = os.path.join("options", "connections.txt")

    with open(txt, "r") as f:
        for line in f:
            line = line.strip()
            points.append(line.split(','))

    grid = {}
    for point in points:
        x = int(point[1])
        y = int(point[2])
        num = int(point[0])
        grid[x, y] = num

    return grid


def get_connections():

    txt = os.path.join("options", "list_1.txt")

    # read the .txt file
    # filter only things inbetween brackets
    with open(txt, "r") as f:
        text = re.findall('\(.*?\)', f.read())

    # make a list of tuples from al connections to make
    connections = []
    for number in text:
        number = number.replace(")", "").replace("(", "").split(",")
        x, y = int(number[0]), int(number[1])
        connections.append([x, y])

    return connections


def matrix(grid):

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
        connection[0] += 1
        connection[1] += 1
        locations.append(
            (coordinates[connection[0]], coordinates[connection[1]]))
        setlist.append(Set(coordinates[connection[0]], coordinates[connection[1]]))
    print("in de init")
    print(matrix[0][8][2])
    return setlist
