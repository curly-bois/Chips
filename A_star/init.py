from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv
import re
import os
import heapq


def get_grid():

    # make a dict of all the points and their location
    points = []

    txt = os.path.join("connections.txt")

    with open(txt, "r") as f:
        for line in f:
            line = line.strip()
            points.append(line.split(','))

    grid = {}
    for point in points:
        x = int(point[1])
        y = int(point[2])
        num = int(point[0])
        grid[x,y] = num

    return grid

def get_connections():

    txt = os.path.join("options", "list_small.txt")

    # read the .txt file
        # filter only things inbetween brackets
    with open(txt, "r") as f:
            text = re.findall('\(.*?\)',f.read())

    # make a list of tuples from al connections to make
    connections = []
    for number in text:
        number = number.replace(")", "").replace("(", "").split(",")
        x,y = int(number[0]),int(number[1])
        connections.append([x,y])

    return connections


def matrix(grid):


    tuplist = []

    for tup in grid:
        tuplist.append(tup)

    x = max(tuplist, key=itemgetter(0))[0] + 1
    y = max(tuplist, key=itemgetter(1))[1] + 1
    matrix = [[0 for x in range(x)]
              for y in range(y)]

    for j in range(y):
        for k in range(x):
            if (k,j) in tuplist:
                matrix[j][k] = grid[k,j]


    # '''
    # Visualize points on the grid
    # '''
    # x +=1
    # x +=1
    #
    # # Convert data to useful data
    # plt.figure(figsize=(16,16))
    # plt.xticks(range(x))
    # plt.yticks(range(y))
    # plt.xlim([-1,x])
    # plt.ylim([-1,y])
    # plt.grid(True)
    # for j in range(y):
    #     for k in range(x):
    #         if (k,j) in tuplist:
    #             plt.text(k,j,matrix[j][k])
    #             plt.scatter(k,j,color='red')
    # plt.show()

    return matrix


def make_conlist(connections,matrix):

    locations = []
    coordinates = {}

    for j in range(len(matrix)):
        for k in range(len(matrix[j])):
            if matrix[j][k] > 0:
                coordinates[matrix[j][k]] = (0,j,k)

    for connection in connections:
        connection[0] += 1
        connection[1] += 1
        locations.append([coordinates[connection[0]],coordinates[connection[1]]])


    print(locations)

if __name__ == '__main__':

    connections = get_connections()
    matrix = matrix(get_grid())
    make_conlist(connections,matrix)
