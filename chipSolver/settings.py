import numpy as np
import random
import pandas as pd
import time
import sys

# File location
filename = "options.xlsx"

settings = sys.argv[2]
print(settings)

df = pd.read_excel(filename, sheet_name=0)
var = df.iloc[int(settings)]
var = [int(i) for i in var]
layer_coef = var[0]
NN_penalty = var[1]

# Settings
layer_multiplier = [var[2],var[3],var[4],var[5],var[6],var[7],var[8]]

# wire_penalty = 0.4
# upper_penalty = 0


def get_distance(matrix, points, p1, p2):
    ver = points.index(p1)
    hor = points.index(p2)
    return matrix[ver][hor]


def sort_points(starts, ends):
    '''
    A way of sorting the points, very easy and not thought out.
    '''
    # Make two indentical list, sort one and use the other for indexing
    distance = [abs(s[0]-e[0])+abs(s[1]-e[1]) for s,e in zip(starts,ends)]
    index = [abs(s[0]-e[0])+abs(s[1]-e[1]) for s,e in zip(starts,ends)]
    distance.sort()
    points_unsorted = list(zip(starts,ends))

    # Sort the starts and ends the same way as the distance, using the indexlist
    points = []
    for item in distance:
        i = index.index(item)
        points.append(points_unsorted[i])
        index[i] = -1

    # return the sorted points
    return points

def sort_points2(starts, ends):
    '''
    A way of sorting the points, very easy and not thought out.
    '''
    # Make two indentical list, sort one and use the other for indexing
    def sorting(d):
        s = d[0]
        e = d[1]
        v = abs(s[0]-s[1])
        h = abs(e[0]-e[1])
        d = v+h
        return (v**2)*(h**2)*d

    points = list(zip(starts, ends))
    points.sort(key=sorting)
    # points.reverse()

    return points

def sort_points_random(starts, ends):
    points_unsorted = list(zip(starts,ends))
    random.shuffle(points_unsorted)
    return points_unsorted

def first_value(size):
    '''
    Very influencial defenition, creates the first instance of the value grid
    At the moment the values are set to 0, testing should result in best values
    '''
    # triple list comperhansion
    super_grid = [[[        1.00 + (abs(y-size[1]/2) + abs(x-size[1]/2)) * (1/size[1])
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]

    # Return a Numpy array (faster)
    super_matrix = np.array(super_grid)

    # layer bonus
    super_matrix *= np.array(layer_multiplier)
    return super_matrix

def second_value(size):
    '''
    Very influencial defenition, creates the first instance of the value grid
    At the moment the values are set to 0, testing should result in best values
    '''
    # triple list comperhansion
    super_grid = [[[        1.00
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]

    # Return a Numpy array (faster)
    super_matrix = np.array(super_grid)

    return super_matrix

def update_layer(layer_info, value_grid):
    '''
    Update layers based on the info it got from the layer info
    '''
    # retrive the count dict
    empty = np.zeros(len(layer_info))

    # Calculate the occupiance of the layer
    for key in layer_info:
        layer_coverage = layer_info[key]['free']/255
        empty[key] = (1) + ((layer_coverage*layer_coef))

    # Matrix multiplication
    value_grid *= empty

    return value_grid

def edit_grid(grid, points, value_grid):
    '''
    Edit the value grid based on the points
    edits the values around the points and above
    '''
    # For every point
    for p in grid:
        p = grid[p]
        if p.location in points:

            # for every neighbour
            for N in p.neighbours:
                x,y,z = N.location
                value_grid[x][y][z] += NN_penalty ## changes to +

            # # for every X points above the point
            # x,y,z = p.location
            # for i in range(2): # This hard coded!!!!!!!!!
            #     value_grid[x][y][i] += upper_penalty*(3-(i+1))*(1/3)

    return value_grid

def wire_NN_edit(grid, value_grid):
    '''
    Edit the values of the neighbours of the wires
    '''
    # for every point
    for p in grid:
        p = grid[p]

        # If it's a wire
        if p.attribute == 'wire':

            # Set all neighbours to 0.1
            for N in p.neighbours:
                x,y,z = N.location
                value_grid[x][y][z] += wire_penalty ## Changed to +++
    return value_grid
