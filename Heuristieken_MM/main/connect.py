import numpy as np
from Classes.point import Point
from Classes.set import Set
from Preprocessing.sort_connections import *

def connect(to_be_connected):
    '''
    to_be_connnected [list of sets]
    '''
    np.random.shuffle(to_be_connected)
    orderlist = []

    for set in to_be_connected:
        orderlist.append(f"({set.get_startpoint().get_id()},{set.get_endpoint().get_id()})")

    all_sets = []
    connected_sets = []

    while to_be_connected:
        route = []
        all_sets.append(to_be_connected[0])

        # make start and end point
        start = all_sets[-1].get_startpoint()
        start.h = 0
        end = all_sets[-1].get_endpoint()
        end.set_attribute("empty")

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
            if tries == 1500:
                end.set_attribute("gate")
                break

            #  if no route append points
            elif len(openlist) == 0:
                end.set_attribute("gate")
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
                all_sets[-1].is_connected = True
                connected_sets.append(all_sets[-1])

                # Retrace final step
                going_back = parent[current]



                #  retrace the rest of the steps
                while going_back is not start:
                    route.append(going_back)
                    going_back.set_attribute("wire")
                    going_back = parent[going_back]


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
    connected_sets = []
    unconnected_sets = []
    for set in all_sets:
        if not set.is_it_connected():
            unconnected_sets.append(set)
        else:
            connected_sets.append(set)

    return all_sets, connected_sets, unconnected_sets
