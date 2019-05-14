import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from wire import Wire
from points import Point

class Grid(object):
    def __init__(self, size, points):
        self.size = size
        self.grid = self.make_grid()
        self.make_neighbours()
        self.points = points
        self.set_points()
        self.value_grid = [[[round(z*0.05 + ((z+1)**2)*0.02 +
                            abs(x - 4.5) * 0.05 + 0.05 +
                            abs(y - 4.5) * 0.05 + 0.05, 2)
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]
        self.edit_grid()

    def make_grid(self):
        size = self.size
        grid = {}
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    grid[(i,j,k)] = Point((i,j,k))
        return grid

    def edit_grid(self):
        for p in self.grid:
            p = self.grid[p]
            if p.location in self.points:
                NN = p.neighbours
                for N in NN:
                    x,y,z = N.location
                    self.value_grid[x][y][z] = 0.001

        return


    def make_neighbours(self):
        # Make neighbours
        for x,y,z in self.grid:
            point = self.grid[(x,y,z)]
            try:
                point.set_neighbour(self.grid[(x+1,y,z)])
            except:
                pass
            try:
                point.set_neighbour(self.grid[(x-1,y,z)])
            except:
                pass
            try:
                point.set_neighbour(self.grid[(x,y+1,z)])
            except:
                pass
            try:
                point.set_neighbour(self.grid[(x,y-1,z)])
            except:
                pass
            try:
                point.set_neighbour(self.grid[(x,y,z-1)])
            except:
                pass
            try:
                point.set_neighbour(self.grid[(x,y,z+1)])
            except:
                pass

    def set_points(self):
        count = 0
        for point in self.grid:
            point = self.grid[point]
            if point.location in self.points:
                count+=1
                point.set_attribute('point')

        print("Their are no duplicates")
        print(len(self.points) == count )

    def find_line(self, start, end):
        # Set key attributes
        self.grid[start].set_attribute('closed')
        self.grid[end].set_attribute('end')

        # Set temp memory variables
        current_point  = self.grid[start]
        found = False
        parent = {}
        while not found:
            NN = current_point.get_neighbours()
            for N in NN:
                if N.attribute == 'end':
                    parent[N.location] = current_point.location
                    print("Found")
                    found = True

                elif N.attribute == "free":
                    N.set_value(self.cal_val(N.location, end, start))
                    N.set_attribute('open')
                    parent[N.location] = current_point.location

            lowest = 999
            for P in self.grid.values():
                if P.attribute == 'open' and P.value < lowest:
                    lowest = P.value
                    lowest_point = P

            try:
                lowest_point.set_attribute('closed')
                current_point = lowest_point
            except:
                found = True
                parent = {}
                print("Error")

        return parent

    def threedimdistance(self, i, j):
        deltaxsquared = (i[0] - j[0]) ** 2
        deltaysquared = (i[1] - j[1]) ** 2
        deltazsquared = (i[2] - j[2]) ** 2
        return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5

    def cal_val(self, tup_cur, tup_end, tup_start):
        dis2end = self.threedimdistance(tup_cur, tup_end)
        dis2start = self.threedimdistance(tup_start, tup_cur)
        x = tup_cur[0]
        y = tup_cur[1]
        z = tup_cur[2]
        value = ( dis2end - dis2start)*self.value_grid[x][y][z]
        return value

    def make_wire(self, start, end, parent):
        cur = self.grid[end].location
        wire = []
        while parent[cur] != start:
            wire.append(cur)
            self.grid[cur].set_attribute('wire')
            cur = parent[cur]

        wire.append(start)
        self.grid[start].set_attribute('wire')

        for P in self.grid.values():
            if P.attribute == 'open' or P.attribute == 'closed':
                P.set_attribute('free')
        return wire

    def plot_wire(self, wires):
        fig = plt.figure()
        wires = [i.route for i in wires]
        data = zip(*wires)

        ax = fig.add_subplot(111, projection='3d')
        for l in wires:
            linex,liney, linez = zip(*l)
            ax.plot(linex, liney,linez, linewidth=5, color='blue')

        px, py, pz = zip(*self.points)
        ax.scatter(px, py, pz, linewidth=10, color='red')
        # draw gridlines
        plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        plt.show()
