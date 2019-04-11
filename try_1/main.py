from point import Point
from init import get_grid
from init import matrix

cube = matrix(get_grid())
print(cube)
print("\n")
print(cube[1][0][3])

start = cube[1][0][3]

# Gets neighbours, checks if gate, if not gate -> go on
# If gate: retrace steps

new_points = 
while not found:
# Checks if one of the neighbours is an unconnected gate
    for neighbour in start.get_neighbours():

        # If one of the neighbours is a gate
        if neighbour.get_attribute() == "gate":
            break

        # If point is empty, append to list
        elif neighbour.get_attribute() == "empty":
            new_points.append(neighbour)
