from operator import itemgetter
import numpy
import matplotlib.pyplot as plt


# LOAD TXT LOCATIONS

# FIND HIGHEST VALUES AND DETERMINE GRID SIZE
netlist_1 = [(23, 4), (5, 7), (1, 0), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 0), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]

max_x = max(netlist_1)[0]
max_y = max(netlist_1, key=itemgetter(1))[1]
print(max_x)
print(max_y)

unconnected_nets = netlist_1
connected_nets = []

wire = []

# start here:
start = min(netlist_1)
wire.append(start)
print(min(netlist_1))

while len(unconnected_nets) > 1:
    # Reset difference
    difference = []


    # find closest net
    unconnected_nets.remove(start)
    connected_nets.append(start)

    print(f"Now there are {len(unconnected_nets)} nets left and {len(connected_nets)} nets are already connected\n")


    # calculates distance form start net to all other unconnected nets
    for net in unconnected_nets:
        diff = sum(abs(numpy.subtract(start, net)))
        difference.append(diff)
    # the minimum difference
    min_difference = min(difference)

    # Finds the position of the closest net in the list of unconnected nets
    closest_index = difference.index(min_difference)
    print(f"This unconnected net is closest now: {unconnected_nets[closest_index]}\n")

    end = unconnected_nets[closest_index]

    # Calculates vertical and horizontal difference
    vertical_difference = numpy.subtract(start, end)[1]
    horizontal_difference = numpy.subtract(start, end)[0]

    # Amount of steps needed to take in vertical and horizontal direction
    vertical_steps = abs(vertical_difference)
    horizontal_steps = abs(horizontal_difference)

    print(f"The amount of steps needed between the start net {start} and end net {end} is {vertical_steps + horizontal_steps}. In vertical direction we need to take {vertical_difference * -1} steps and in horizontal direction we need to take {horizontal_difference * -1} steps\n")


    # While there are still steps to be taken to get to the next net
    while(vertical_steps > 0 or horizontal_steps > 0):
        # Take a vertical step if more vertical steps are needed than horizontal steps
        if vertical_steps > horizontal_steps:
            # Step up
            if vertical_difference < 0:
                step = (wire[-1][0], wire[-1][1]+1)
                wire.append(step)
            # Step up
            else:
                step = (wire[-1][0], wire[-1][1]-1)
                wire.append(step)

            vertical_steps -= 1

        # Take a horizontal step if more horizontal steps are needed than vertical steps
        elif horizontal_steps > vertical_steps:
            # Step to the right
            if horizontal_difference < 0:
                step = (wire[-1][0]+1, wire[-1][1])
                wire.append(step)
            # Step to the left
            else:
                step = (wire[-1][0]-1, wire[-1][1])
                wire.append(step)

            horizontal_steps -= 1

        # If an equal amount of steps need to be taken, take a vertical step
        else:
            # Step down
            if vertical_difference < 0:
                step = (wire[-1][0], wire[-1][1]+1)
                wire.append(step)
            # Step up
            else:
                step = (wire[-1][0], wire[-1][1]-1)
                wire.append(step)

            vertical_steps -= 1



    # Set new start net to where we just ended
    start = wire[-1]


unconnected_nets.remove(start)
connected_nets.append(start)
print(f"Now there are {len(unconnected_nets)} nets left and {len(connected_nets)} nets are already connected\n")


# Go back to the first net
start = connected_nets[-1]
end = connected_nets[0]

# Calculates vertical and horizontal difference
vertical_difference = numpy.subtract(start, end)[1]
horizontal_difference = numpy.subtract(start, end)[0]

# Amount of steps needed to take in vertical and horizontal direction
vertical_steps = abs(vertical_difference)
horizontal_steps = abs(horizontal_difference)

# While there are still steps to be taken to get to the next net
while(vertical_steps > 0 or horizontal_steps > 0):
    # Take a vertical step if more vertical steps are needed than horizontal steps
    if vertical_steps > horizontal_steps:
        # Step up
        if vertical_difference < 0:
            step = (wire[-1][0], wire[-1][1]+1)
            wire.append(step)
        # Step up
        else:
            step = (wire[-1][0], wire[-1][1]-1)
            wire.append(step)

        vertical_steps -= 1

    # Take a horizontal step if more horizontal steps are needed than vertical steps
    elif horizontal_steps > vertical_steps:
        # Step to the right
        if horizontal_difference < 0:
            step = (wire[-1][0]+1, wire[-1][1])
            wire.append(step)
        # Step to the left
        else:
            step = (wire[-1][0]-1, wire[-1][1])
            wire.append(step)

        horizontal_steps -= 1

    # If an equal amount of steps need to be taken, take a vertical step
    else:
        # Step down
        if vertical_difference < 0:
            step = (wire[-1][0], wire[-1][1]+1)
            wire.append(step)
        # Step up
        else:
            step = (wire[-1][0], wire[-1][1]-1)
            wire.append(step)

        vertical_steps -= 1



# Set new start net to where we just ended
start = wire[-1]

print(f"The last net {start} has to loop back to the first {end} and takes {vertical_steps + horizontal_steps} steps. In vertical direction we need to take {vertical_difference * -1} steps and in horizontal direction we need to take {horizontal_difference * -1} steps\n")




print(f"The wire takes the following route: {wire} and takes {len(wire)-1} pieces of wire to complete\n")

# Setup
plt.figure(figsize=(16,16))
plt.xticks(range(max_x))
plt.yticks(range(max_y))
plt.xlim([-1,max_x])
plt.ylim([-1,max_y])
plt.grid(True)

netlist_1 = [(23, 4), (5, 7), (1, 0), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 0), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]
# Punten
x,y = zip(*netlist_1)
plt.scatter(x, y, linewidths=10, color='red')

# Lijnen

linex,liney = zip(*wire)
plt.plot(linex, liney, linewidth=5, color='blue')

# linex,liney = zip(*lines[c])
# plt.plot(linex, liney, linewidth=5, color='blue')
# c+=1

plt.show()
