from point import Point
from set import Set
from init import *

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

# initializing the grid and making the points
connections = get_connections()
matrix = matrix(get_grid())
to_be_connected = make_conlist(connections, matrix)

# shuffle the points randomly
np.random.shuffle(to_be_connected)
not_connected = []
all_sets = []

while to_be_connected:
    route = []
    all_sets.append(to_be_connected[0])

    # make start and end point
    start = all_sets[-1].get_startpoint()
    start.h = 0
    end = all_sets[-1].get_endpoint()
    end.attribute = "empty"
    print(f"Start location is: {start.location}")
    print(f"End location is: {end.location}")

    found = False

    wire = []

    # Removes first set
    removed_set = to_be_connected.pop(0)

    openlist = {}
    closedlist = []
    parent = {}

    # loop trough neighbours and append them to the openlist
    # also append startpoint to parent dict
    for neighbour in start.get_neighbours():
        parent[neighbour] = start
        neighbour.h = start.h + 1
        openlist[neighbour] = neighbour.calculate_f(start.get_location(),
                                                    end.get_location())

    # append start to closed list for it is visited
    closedlist.append(start)

    # set tries to 0
    tries = 0

    while not found:
        tries += 1

        # try N amount of times
        if tries == 500:
            print("Tried 3000 times")
            print(len(to_be_connected))
            not_connected.append([start.id, end.id])
            break

        #  if no route append points
        if len(openlist) == 0:
            print("HELAAS")
            not_connected.append([start.id, end.id])
            break

        # get the lowest f value of the openlist, make this current
        current = min(openlist, key=openlist.get)

        # get the lowest F value
        lowest_f = openlist[current]

        #  make list of the lowest f values
        lowest_fs = []

        # make list of lowest f values
        for point in openlist:
            if openlist[point] <= lowest_f:
                lowest_fs.append(point)

        # If there are multiple points with the lowest f value, go to lowest h
        if len(lowest_fs) > 1:
            h_vals = {}
            for point in lowest_fs:
                h_vals[point] = point.get_h()

        # print(f"lowest in openlist is now: {current.get_location()} with an f of {current.calculate_f(start.get_location(), end.get_location())}")

        # delete the current postion from openlist
        del openlist[current]
        closedlist.append(current)

        # if current is the end, set ths as taken
        if current == end:
            end.attribute = "taken"
            start.attribute = "taken"
            print("End has been found")
            all_sets[-1].is_connected = True

            # Retrace final step
            going_back = parent[current]

            route.append(end)

            #  retrace the rest of the steps
            while going_back is not start:
                route.append(going_back)
                going_back.set_attribute("wire")
                print(f"Retracing steps: {going_back.location}")
                going_back = parent[going_back]

            route.append(start)
            all_sets[-1].set_route(list(reversed(route)))
            found = True

            break

        for neighbour in current.get_neighbours():
            if neighbour.get_attribute() != "empty" or neighbour in closedlist:
                continue

            if neighbour not in openlist:
                parent[neighbour] = current
                neighbour.h = current.h + 1
                openlist[neighbour] = neighbour.calculate_f(start.get_location(),
                                                            end.get_location())

#  make the plot
wires = []
taken = []
wire_pieces = 0
for three_dimensions in matrix:
    for two_dimensions in three_dimensions:
        for point in two_dimensions:
            if point.get_attribute() == "wire":
                wires.append(point.location)
                wire_pieces += 1
            if point.get_attribute() == "taken" or point.get_attribute() == "gate":
                taken.append(point.location)

print(not_connected)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_zlim(0, 6)
ax.scatter3D(*zip(*wires))
ax.scatter3D(*zip(*taken))
plt.show()

for set in all_sets:
    print(set)
