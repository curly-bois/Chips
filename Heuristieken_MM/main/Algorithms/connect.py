from Preprocessing.init import *
from Classes.point import Point
from Classes.set import Set
import numpy as np

def connect(to_be_connected):
    '''
    this is the A/A* algortithm which finds either the shortest route or the
    best route according to the given extra heuristics
    '''

    all_sets = []
    connected_sets = []
    unconnected_sets = []

    # loop through the netlist
    for set in to_be_connected:

        # if the set of points is not connected, start finding a route.
        if set.is_it_connected() == False:

            # make start and end point
            start = set.get_startpoint()
            end = set.get_endpoint()
            end.set_attribute("empty")

            # make the heuristic value for the start point 0
            start.f = 0
            found = False

            # make the openlist(non-visited places),closedlist(visited places)
            openlist = {}
            closedlist = []

            # make a parent dict for retracing the steps
            parent = {}

            # loop trough neighbours and append them to the openlist
            # also append startpoint to parent dict
            for neighbour in start.get_neighbours():
                if neighbour.get_attribute() == "empty":
                    parent[neighbour] = start
                    neighbour.f = start.f + 1
                    openlist[neighbour] = neighbour.calculate_h(start.get_location(),
                                                                end.get_location())

            # append start to closed list for it is visited
            closedlist.append(start)

            tries = 0

            while not found:
                tries += 1

                # try N amount of times.
                # if not sucseeded append to the unconnected list
                if tries == 2000:
                    end.set_attribute("gate")
                    unconnected_sets.append(set)
                    break

                #  if all the points on the grid have been visited-
                # append to the unconnected sets
                elif len(openlist) == 0:
                    end.set_attribute("gate")
                    unconnected_sets.append(set)
                    break

                # look for the point with lowest f value of the openlist.
                current = min(openlist, key=openlist.get)

                # get the point with the lowest F value
                lowest_h = openlist[current]

                #  make list of the lowest f values
                lowest_hs = []

                # make list of lowest f values
                for point in openlist:
                    if openlist[point] <= lowest_h:
                        lowest_hs.append(point)

                # If there are multiple points with the lowest h value, go to lowest f
                if len(lowest_hs) > 1:
                    f_vals = {}
                    for point in lowest_hs:
                        f_vals[point] = point.get_f()

                # delete the current postion from openlist
                del openlist[current]
                closedlist.append(current)

                # if current is the end, set ths as taken
                if current == end:
                    end.set_attribute("taken")
                    start.set_attribute("taken")
                    set.is_connected = True
                    connected_sets.append(set)

                    # Retrace final step
                    going_back = parent[current]

                    # get the route and add it to the set class
                    route = []

                    #  retrace the rest of the steps
                    while going_back is not start:
                        if going_back.get_attribute() != "gate":
                            route.append(going_back)
                            going_back.set_attribute("wire")
                            going_back = parent[going_back]

                    set.set_route(list(reversed(route)))
                    found = True

                    break

                # if the end is not found look at he neighbours again
                for neighbour in current.get_neighbours():
                    if neighbour.get_attribute() != "empty" or neighbour in closedlist:
                        continue

                    elif neighbour not in openlist:
                        parent[neighbour] = current
                        neighbour.f = current.f + 1
                        openlist[neighbour] = neighbour.calculate_h(start.get_location(),
                                                                    end.get_location())


    return to_be_connected, connected_sets, unconnected_sets
