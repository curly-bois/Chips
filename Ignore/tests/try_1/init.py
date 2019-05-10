from operator import itemgetter
import re
import os
import itertools
from point import Point

def amount_of_gates():
    return len(tuplist)

def get_grid():
    # read the .txt file
    txt = os.path.join("list_2.txt")
    with open(txt, "r") as f:
        # filter only things inbetween brackets
        text = re.findall('\(.*?\)',f.read())

    grid = []

    for number in text:
        number = number.replace(")", "")
        number = number.replace("(", "")
        number = number.split(",")
        x = int(number[0])
        y = int(number[1])
        tuplist = [x,y]
        grid.append(tuplist)

    return grid

def matrix(grid):

    z = 3

    tuplist = []
    for tup in grid:
        tuplist.append(tuple(tup))
    x = max(tuplist, key=itemgetter(0))[0] + 1
    y = max(tuplist, key=itemgetter(1))[1] + 1

    print(x,y)
    print(tuplist)

    matrix = [[[0 for x in range(x)]
              for y in range(y)]
              for z in range(z)]

    for i in range(z):
        for j in range(y):
            for k in range(x):

                # Point in 3d matrix is a gate
                if tuple([k,j]) in tuplist and i == 1:
                    matrix[i][j][k] = Point((k, j, i), "gate", [], 0)
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
                    neighbours.append(matrix[i][j+1][k])

                # Eastern neighbour
                if k + 1 < x:
                    neighbours.append(matrix[i][j][k+1])

                # Southern neighbour
                if j - 1 >= 0:
                    neighbours.append(matrix[i][j-1][k])

                # Western neighbour
                if k - 1 >= 0:
                    neighbours.append(matrix[i][j][k-1])

                # Upper neighbour
                if i + 1 < z:
                    neighbours.append(matrix[i+1][j][k])

                # Down neighbour
                if i - 1 >= 0:
                    neighbours.append(matrix[i-1][j][k])

                matrix[i][j][k].set_neighbours(neighbours)
                if matrix[i][j][k].attribute == "gate":
                    gates.append(matrix[i][j][k].location)

    print(gates)

    return matrix, len(tuplist)


    # for i in range(z):
    #     print()
    #     for j in range(y):
    #         print(matrix[i][j])

matrix(get_grid())
