import numpy as np
import random
import pandas as pd
import time

from extra import *

# File location
filename = "book2.xlsx"

# Settings
layer_multiplier = [1,1,1,1,1,1,1]
layer_coef = 0.05

NN_penalty = 3
# wire_penalty = 0.4
# upper_penalty = 0

option = {'layer_multiplier':str(layer_multiplier), 'layer_coef':layer_coef, 'NN_penalty': NN_penalty}
def save_option(filename, option):
    df = pd.read_excel(filename, sheet_name=0)
    option['time'] = str(time.localtime())
    df_new = pd.DataFrame(option, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.to_excel(filename)

def get_distance(matrix, points, p1, p2):
    ver = points.index(p1)
    hor = points.index(p2)
    return matrix[ver][hor]

def cal_val(value_grid, cur, tup_end, tup_start, current_point):
    '''
    Calculate the values for the Astar Algo
    '''
    tup_cur = cur.location

    # Get distance values
    dis2end = threedimdistance(tup_cur, tup_end)
    # dis2end = get_distance(matrix, points, tup_cur, tup_end)

    dis2start = current_point.g + 1
    cur.setG(dis2start)

    # Get coordinates
    x,y,z = tup_cur[0],tup_cur[1],tup_cur[2]

    # Adjust for value_grid
    value = (dis2end + dis2start)*float(value_grid[x][y][z])
    return (value, dis2end)

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
    super_grid = [[[        1.00
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]

    # Return a Numpy array (faster)
    super_matrix = np.array(super_grid)

    # layer bonus
    super_matrix *= np.array(layer_multiplier)
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

save_option(filename, option)
