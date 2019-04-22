from point import Point
from grid import Grid
from wire import Wire

from extra import *

SIZE = (17,17,7)
NUMBER = 50

starts, ends = make_random_points(SIZE, resolution=2, number=NUMBER)

points = [(1,1),(6,1),(10,1),(15,1),(3,2),(12,2),(14,2),(1,3),(6,3),(12,3),
          (15,3),(2,4),(8,4),(1,5),(4,5),(10,5),(11,5),(16,5),(2,6),(7,6),
          (10,6),(12,6),(15,6),(6,7),(13,7),(16,7),(6,8),(7,8),(9,8),(11,8),
          (15,8),(1,9),(6,9),(9,10),(12,11),(2,12),(4,12),(7,12),(10,12),
          (15,12),(9,13),(13,13),(4,14),(6,14),(1,15),(6,15),(8,15),(11,15),
          (13,15),(16,15)]

netlist_4 = [(42, 3), (3, 48), (14, 6), (36, 2), (14, 4), (10, 32), (47, 22),
             (41, 1), (21, 6), (39, 18), (22, 49), (35, 14), (5, 31), (48, 24),
             (12, 14), (8, 42), (28, 43), (20, 40), (26, 24), (46, 35), (0, 12),
             (46, 12), (35, 26), (21, 7), (43, 15), (0, 21), (35, 19), (31, 11),
             (43, 30), (12, 1), (4, 30), (49, 13), (4, 29), (8, 28), (32, 29),
             (34, 45), (14, 39), (17, 25), (28, 27), (31, 25), (37, 16), (2, 3),
             (3, 31), (4, 23), (5, 44), (33, 30), (36, 4), (29, 9), (46, 0),
             (39, 15)]

starts,ends = make_imported_points(points, netlist_4)

# Normal order, or custom order
# points_to_connect = zip(starts,ends)
points_to_connect = sort_points(starts, ends)

# Initialize the grid
points = starts+ends
mainGrid = Grid(SIZE, points)

# Start the loop for all the wires
wires = []
total_points = len(points_to_connect)
connected = 0

for start,end in points_to_connect:
    # find line, else return empty dict
    parent, tries = mainGrid.find_line(start, end)
    if parent == {}:
        pass
    else:
        # Retrace the line and laydown the wire
        wire = mainGrid.make_wire(start, end, parent)
        con_wire = Wire(start, end, wire, tries)
        wires.append(con_wire)
        # Update value grid
        mainGrid.update_layer()
        # mainGrid.wire_NN_edit()
        connected += 1

# Print lenght + minimal lenght
length_score(wires, connected/total_points)

# Plots result
mainGrid.plot_wire(wires)
