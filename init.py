import matplotlib.pyplot as plt
import re

def get_grid():
    # read the .txt file
    with open("grids.txt", "r") as f:
        # filter only things inbetween brackets
        text = re.findall('\(.*?\)',f.read())

    highX = 0
    highY = 0
    grid = []
    for number in text:
        number = number.replace(")", "")
        number = number.replace("(", "")
        number = number.split(",")
        x = int(number[0])
        y = int(number[1])
        tuplist = [x,y]
        grid.append(tuple(tuplist))
        if x > highX:
            highX = x
        if y > highY:
            highY = y

    return grid, highX, highY

def make_grid(grid, sizex, sizey):
    '''
    Visualize points on the grid
    '''
    # Convert data to useful data
    sizex += 1
    sizey += 1
    x,y = zip(*grid)

    # Setup
    plt.figure(figsize=(16,16))
    plt.xticks(range(sizex))
    plt.yticks(range(sizey))
    plt.xlim([-1,sizex])
    plt.ylim([-1,sizey])
    plt.grid(True)
    # scatter points
    plt.figure(figsize=(16,16))
    plt.scatter(x, y, linewidths=8, color='red')

    plt.show()

if __name__ == '__main__':

    make_grid(get_grid()[0],get_grid()[1],get_grid()[2])
