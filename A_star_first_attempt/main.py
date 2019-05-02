from point import Point
from init_2 import *

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys


connections = get_connections()
matrix = matrix(get_grid())
to_be_connected = make_conlist(connections,matrix)

print(to_be_connected)
np.random.shuffle(to_be_connected)
print("***")

print("\n\n\n ***********************************************************")


# Gets neighbours, checks if gate, if not gate -> go on
# If gate: retrace steps

# to_be_connected = [(cube[0][10][9], cube[0][1][15])]



# While
while to_be_connected:
    print("***********************************************************")
    print("***********************************************************")
    print("***********************************************************")
    print(f"Amount of sets to be connected: {len(to_be_connected)}")
    print("***********************************************************")
    print("***********************************************************")
    print("***********************************************************")
    start = to_be_connected[0][0]
    start.h = 0
    end = to_be_connected[0][1]
    end.attribute = "empty"
    print(f"Start location is: {start.location}")
    print(f"End location is: {end.location}")

    found = False

    wire = []

    # Removes first set
    to_be_connected.pop(0)

    openlist = {}
    closedlist = []
    parent = {}

    for neighbour in start.get_neighbours():
        parent[neighbour] = start
        neighbour.h = start.h + 1
        openlist[neighbour] = neighbour.calculate_f(start.get_location(),
                                                    end.get_location())
    closedlist.append(start)
    #print(f"This is openlist {openlist}")

    tries = 0
    while not found:
        tries += 1
        if tries == 2000:
            print("Tried 500 times")
            print(len(to_be_connected))
            sys.exit()

        current = min(openlist, key=openlist.get)

        lowest_f = openlist[current]

        lowest_fs = []

        for point in openlist:
            if openlist[point] == lowest_f:
                lowest_fs.append(point)

        # If there are multiple points with the lowest f value, go to lowest h
        if len(lowest_fs) > 1:
            h_vals = {}
            for point in lowest_fs:
                h_vals[point] = point.get_h()

            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            current = min(h_vals, key=h_vals.get)
            print(f"There is a lower h: {current.get_location()}")


        print(f"lowest in openlist is now: {current.get_location()} with an f of {current.calculate_f(start.get_location(), end.get_location())}")

        del openlist[current]
        closedlist.append(current)
        #print(f"This is openlist {openlist}")

        if current == end:
            end.attribute = "taken"
            start.attribute = "taken"
            print("End has been found")
            # Retrace steps
            going_back = parent[current]

            while going_back is not start:
                going_back.set_attribute("wire")
                print(f"Retracing steps: {going_back.location}")
                going_back = parent[going_back]

            found = True

            ## TESTER ##

            # tester+=1
            # if tester == 3:
            #     exit()


            break

        for neighbour in current.get_neighbours():
            if neighbour.get_attribute() != "empty" or neighbour in closedlist:
                continue

            if neighbour not in openlist:
                parent[neighbour] = current
                neighbour.h = current.h + 1
                openlist[neighbour] = neighbour.calculate_f(start.get_location(),
                                                            end.get_location())

print("All sets have been connected")

#
#
#     while not found:
#
#         for point in openlist:
#             this_point = openlist.remove(point)
#             closed_list.append(this_point)
#
#         # Checks if one of the neighbours is an unconnected gate
#             for neighbour in point.get_neighbours():
#
#                 flist[neighbour] = neighbour.calculate_f()
#                 lowest_f = min(flist.values())
#                 openlist.append(neighbour)
#
#             for key, value in flist.iteritems():
#                 if value == lowest_f:
#                     next_step = key
#
#             # Get lowest value for all points in openlist
#             for point in openlist:
#                 these_fs.append(flist[point])
#
#             next_point = openlist(min(these_fs).index())
#
#             print(f"The next point with the lowest f value is {next_point}")
#
#             openlist.remove(next_point)
#             closedlist.append(next_point)
#
#
#
#
#             # If one of the neighbours is a gate
#             if neighbour == end: # !!! make sure end is 3D
#                 parents[neighbour] = point
#                 print(f"gate was found at location {neighbour.location}")
#
#                 # Retrace steps
#                 going_back = parents[neighbour]
#                 while going_back is not start:
#                     going_back.set_attribute("wire")
#                     print(f"Retracing steps: {going_back.location}")
#                     going_back = parents[going_back]
#
#
#                 print("gate was found") # !!!
#                 start = neighbour
#                 found = True
#                 print("point is found, breaking out of inner loop")
#                 break
#
#             # If point is empty, append to list
#             elif neighbour.get_attribute() == "empty":
#                 parents[neighbour] = point
#                 next_points.append(neighbour)
#                 queue.append(neighbour)
#
#         # The new next points
#         new_points = next_points
#
#
wires = []
taken = []
wire_pieces = 0
for three_dimensions in matrix:
    for two_dimensions in three_dimensions:
        for point in two_dimensions:
            if point.get_attribute() == "wire":
                wires.append(point.location)
                print(point.location)
                wire_pieces += 1
            if point.get_attribute() == "taken" or point.get_attribute() == "gate":
                taken.append(point.location)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_zlim(0, 6)
print(wires)
ax.scatter3D(*zip(*wires))
ax.scatter3D(*zip(*taken))
plt.show()


# midlayer = []
#
#
# for point in wires:
#     if point[2] == 1:
#         midlayer.append((point[0], point[1]))
#
# print(midlayer)
#
# x,y = zip(*midlayer)
# plt.scatter(x, y, linewidths=2, color='red')
# plt.show()
#
# linex,liney = zip(*midlayer)
# plt.plot(linex, liney, linewidth=5, color='blue')
# plt.show()
#
# print(f"{wire_pieces} pieces of wire used")
