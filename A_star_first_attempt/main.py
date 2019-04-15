from point import Point
from init import get_grid
from init import matrix
from init import amount_of_gates

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys

cube, amount_of_unconnected_gates, tuplist = matrix(get_grid())

print("\n\n\n ***********************************************************")


# Gets neighbours, checks if gate, if not gate -> go on
# If gate: retrace steps

to_be_connected = [(cube[0][0][3], cube[0][6][11]), (cube[0][12][6], cube[0][15][6]),
                    (cube[0][10][8], cube[0][7][1]), (cube[0][13][5], cube[0][4][8]),
                    (cube[0][19][12], cube[0][8][13]), (cube[0][14][4], cube[0][19][18]),
                    (cube[0][2][20], cube[0][9][14]), (cube[0][15][2], cube[0][3][10]),
                    (cube[0][11][5], cube[0][6][16]), (cube[0][16][16], cube[0][12][2])]

wirelines = []

# While
while to_be_connected:
    print(f"Amount of sets to be connected: {len(to_be_connected)}")
    start = to_be_connected[0][0]
    end = to_be_connected[0][1]

    found = False

    wire = []

    # Removes first set
    to_be_connected.pop(0)

    openlist = {}
    closedlist = []
    parent = {}

    for neighbour in start.get_neighbours():
        parent[neighbour] = start
        openlist[neighbour] = neighbour.calculate_f(start.get_location(),
                                                    end.get_location())
    closedlist.append(start)
    print(f"This is openlist {openlist}")

    tries = 0
    while not found:
        tries += 1
        if tries == 500:
            print("Tried 500 times")
            sys.exit()

        current = min(openlist, key=openlist.get)
        print(current)

        del openlist[current]
        closedlist.append(current)
        print(f"This is openlist {openlist}")

        if current == end:
            wire.append(end.get_location())
            end.attribute = "taken"
            start.attribute = "taken"
            print("End has been found")
            # Retrace steps
            going_back = parent[current]

            while going_back is not start:
                wire.append(going_back.get_location())
                going_back.set_attribute("wire")
                print(f"Retracing steps: {going_back.location}")
                going_back = parent[going_back]

            wire.append(start.get_location())
            wirelines.append(wire)
            found = True
            break

        for neighbour in current.get_neighbours():
            if neighbour.get_attribute() != "empty" or neighbour in closedlist:
                continue

            if neighbour not in openlist:
                parent[neighbour] = current
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
for three_dimensions in cube:
    for two_dimensions in three_dimensions:
        for point in two_dimensions:
            if point.get_attribute() == "wire":
                wires.append(point.location)
                print(point.location)
                wire_pieces += 1
            if point.get_attribute() == "taken":
                taken.append(point.location)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_zlim(0, 2)
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
