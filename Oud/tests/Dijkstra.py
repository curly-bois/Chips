import matplotlib.pyplot as plt
import re
import os
import itertools
import heapq

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

    return dict, highX, highY

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
       # x = data_dict.keys()
       # y = data_dict.values()
        plt.text(x[0],y[0],data)
        plt.scatter(x,y,color='red')
    plt.show()

def check_route(dict):

    visited = {}
    unvisited = {}
    # making a list of tuples for the unvisited bridges
    for point in dict:
        unvisited[point] = tuple(dict[point])
    position = 1
    visited[1] = unvisited[1]
    del unvisited[1]
    distance = {}
    closest = []

    # TODO: make it a loop
    # look at the distance from all points
    for point in unvisited:
        x = abs(unvisited[point][0] - visited[position][0])
        y = abs(unvisited[point][1] - visited[position][1])
        distance[point] = x+y

    # get the 5 closest points check all possible routes
    closest = heapq.nsmallest(5, distance, key=distance.get)
    options = list(itertools.permutations(closest))

    route = {}
    # check all distances from possible routes
    for option in options:
        values = 0
        option = list(option)
        option = [position] + option

        for i in range(len(option) - 1):
            x = abs(dict[option[i]][0] - dict[option[i+1]][0])
            y = abs(dict[option[i]][1] - dict[option[i+1]][1])
            value = x + y
            values = values + value
        route[tuple(option)] = values

    # get the shortest 3 routes
    shortest = heapq.nsmallest(3, route, key=route.get)

    for i in shortest:
        print(i)
        print(i[-1])
        print(route[i])




if __name__ == '__main__':

     # make_grid(get_grid()[0],get_grid()[1],get_grid()[2])
     check_route(get_grid()[0])
