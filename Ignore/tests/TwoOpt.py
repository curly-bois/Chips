import matplotlib.pyplot as plt
from operator import itemgetter
import re
import os
import itertools


def get_grid():
    # read the .txt file
    txt = os.path.join("options", "list_1.txt")
    with open(txt, "r") as f:
        # filter only things inbetween brackets
        text = re.findall('\(.*?\)',f.read())

    highX = 0
    highY = 0
    grid = []
    dict = {}
    num = 1
    for number in text:
        number = number.replace(")", "")
        number = number.replace("(", "")
        number = number.split(",")
        x = int(number[0])
        y = int(number[1])
        tuplist = [x,y]
        grid.append(tuplist)
        if x > highX:
            highX = x
        if y > highY:
            highY = y
        dict[num] = tuplist
        num += 1

    return dict, highX, highY, grid

def make_grid(dict, sizex, sizey):
    '''
    Visualize points on the grid
    '''
    # Convert data to useful data
    sizex += 1
    sizey += 1

    plt.figure(figsize=(16,16))
    plt.xticks(range(sizex))
    plt.yticks(range(sizey))
    plt.xlim([-1,sizex])
    plt.ylim([-1,sizey])
    plt.grid(True)

    for data in dict:
        x,y = zip(dict[data])
        plt.text(x[0],y[0],data)
        plt.scatter(x,y,color='red')
    plt.show()

def matrix(grid):
    tuplist = []
    for tup in grid:
        tuplist.append(tuple(tup))
    x = max(tuplist, key=itemgetter(0))[0]
    y = max(tuplist, key=itemgetter(1))[1]

    matrix = [[0 for x in range(x)]
              for y in range(y)]


    for i in range(y):
        for j in range(x):
            if tuple([j,i]) in tuplist:
                matrix[i][j] = 1

    for i in range(y):
        print(matrix[i])






if __name__ == '__main__':

    dict,sizex,sizey,grid = get_grid()
    matrix(grid)
    make_grid(dict,sizex,sizey)
