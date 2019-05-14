from grid import Grid
from wire import Wire
from points import Point
from extras import sort_points


# initial
starts = [(1,1,0),(5,1,0),(5,5,0),(4,2,0),(1,4,0),(5,9,0),(9,9,0),(1,2,0),(10,10,0),(11,2,0),(12,7,0),(8,14,0),(13,4,0),(6,7,0)]
ends = [(8,8,0),(1,9,0),(4,9,0),(5,8,0),(3,1,0),(9,2,0),(2,8,0),(3,4,0),(11,12,0),(1,13,0),(9,8,0),(13,5,0),(14,14,0),(12,8,0)]

size = (15,15,7)

wires = []
# points_to_connect = zip(starts,ends)
points_to_connect = sort_points(starts, ends)
points = starts+ends
mainGrid = Grid(size, points)

# for p in mainGrid.grid:
#     print(mainGrid.grid[p].attribute, mainGrid.grid[p].location)

for start,end in points_to_connect:
    parent = mainGrid.find_line(start, end)
    if parent == {}:
        pass
    else:
        wire = mainGrid.make_wire(start, end, parent)
        con_wire = Wire(start, end, wire)
        wires.append(con_wire)

## Cross Check
all = []
for w in wires:
    all += w.route

print('\nNothing is crossing')
print(len(all) == len(set(all)), '\n')

mainGrid.plot_wire(wires)
