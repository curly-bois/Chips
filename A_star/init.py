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

    print(x,y)

    for j in range(y):
        for k in range(x):
            if (k,j) in tuplist:
                matrix[j][k] = grid[k,j]

    for j in range(y):
        print(matrix[j])


    fig, ax = plt.subplots()
    cmap = mcolors.ListedColormap(['w','r'])
    bounds = [0,0.5,0.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(matrix,cmap=cmap, norm=norm)

    # We want to show all ticks...
    ax.set_xticks(np.arange(x))
    ax.set_yticks(np.arange(y))
    # ... and label them with the respective list entries
    ax.set_xticklabels(range(x))
    ax.set_yticklabels(range(y))

    '''
    Visualize points on the grid
    '''
    # Convert data to useful data
    x += 1
    y += 1
    px,py = zip(*grid)

    # Setup
    plt.figure(figsize=(16,16))
    plt.xticks(range(x))
    plt.yticks(range(y))
    plt.xlim([-1,x])
    plt.ylim([-1,y])
    plt.grid(True)
    plt.scatter(px, py, linewidths=8, color='red')

    plt.show()

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(y):
        for j in range(x):
             if (j,i) in tuplist:
                 text = ax.text(j, i, matrix[i][j],
                               ha="right", va="top", color="black")


    ax.set_title("Print #1")
    fig.tight_layout()

    # turn off the axis labels
    ax.axis('off')
    plt.show()








if __name__ == '__main__':

    get_connections()
    matrix(get_grid())
