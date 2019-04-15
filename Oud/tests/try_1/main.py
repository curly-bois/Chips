from point import Point
from init import get_grid
from init import matrix
from init import amount_of_gates

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

cube, amount_of_unconnected_gates = matrix(get_grid())

print(cube)
print("\n")
print(cube[1][0][3])

start = cube[1][0][3]
first_location = start
amount_of_unconnected_gates -= 1


# Gets neighbours, checks if gate, if not gate -> go on
# If gate: retrace steps

# While
while True:
    print(f"Amount of unconnected gates: {amount_of_unconnected_gates}")
    if amount_of_unconnected_gates == 0:
        break

    new_points = []
    next_points = []
    queue = []
    parents = {}
    new_points.append(start)
    queue.append(start)
    start.set_attribute("taken")
    amount_of_unconnected_gates -= 1
    found = False
    while not found:

        for point in new_points:
            if found:
                print("point is found, breaking out of this loop as well")
                break
        # Checks if one of the neighbours is an unconnected gate
            for neighbour in point.get_neighbours():

                # Continues to next neighbour if neighbour is already in queue
                if neighbour in queue:
                    continue

                # If one of the neighbours is a gate
                if neighbour.get_attribute() == "gate":
                    parents[neighbour] = point
                    print(f"gate was found at location {neighbour.location}")

                    # Retrace steps
                    going_back = parents[neighbour]
                    while going_back is not start:
                        going_back.set_attribute("wire")
                        print(f"Retracing steps: {going_back.location}")
                        going_back = parents[going_back]


                    print("gate was found") # !!!
                    start = neighbour
                    found = True
                    print("point is found, breaking out of inner loop")
                    break

                # If point is empty, append to list
                elif neighbour.get_attribute() == "empty":
                    parents[neighbour] = point
                    next_points.append(neighbour)
                    queue.append(neighbour)

        # The new next points
        new_points = next_points


print("all gates connected")
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

midlayer = []


for point in wires:
    if point[2] == 1:
        midlayer.append((point[0], point[1]))

print(midlayer)

x,y = zip(*midlayer)
plt.scatter(x, y, linewidths=2, color='red')
plt.show()

linex,liney = zip(*midlayer)
plt.plot(linex, liney, linewidth=5, color='blue')
plt.show()

print(f"{wire_pieces} pieces of wire used")
