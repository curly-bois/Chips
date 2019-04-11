from operator import itemgetter
import re
import os
import itertools


def get_grid():
    # read the .txt file
    txt = os.path.join("list_1.txt")
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
                if tuple([k,j]) in tuplist:
                    matrix[1][j][k] = 1

    for i in range(z):
        print()
        for j in range(y):
            print(matrix[i][j])



if __name__ == '__main__':

    matrix(get_grid())
