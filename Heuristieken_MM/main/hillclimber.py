import numpy as np
from connect import connect
import random
import math
from init import *

def hillsolve(max_tries, matrix, all_sets, unconnected_sets, connected_sets):
    hilltries = 0
    test = 0

    while len(unconnected_sets) > 0 and hilltries < max_tries:
        hilltries += 1


        connected = []
        unconnected = []

        for set in all_sets:
            if set.is_it_connected() == True:
                connected.append(set)
                set.was_connected = True
                set.set_old_route(set.get_route())
            elif set.is_it_connected() == False:
                unconnected.append(set)
                set.was_connected = False

        print(f"after try {hilltries}, {int(len(unconnected) / len(all_sets) * 100)}% is unconnected")

        np.random.shuffle(all_sets)

        new_connections = []
        broken_sets = []

        counter = 0
        i = 0
        sets_to_be_broken = int(len(connected) * 0.3)

        while counter < sets_to_be_broken:
            if all_sets[i].is_it_connected() == True:
                all_sets[i].disconnect()
                counter += 1
                i += 1
            else:
                i += 1

        if hilltries < 15:
            all_sets = new_order(all_sets)
        elif hilltries < 25:
            all_sets = make_order(all_sets)
        else:
            np.random.shuffle(all_sets)

        all_sets, new_connected_sets, new_unconnected_sets = connect(all_sets)

        if len(new_unconnected_sets) == 0:
            wire_count = 0
            for set in all_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            print(f"ALTERNATIVE COUNT, SOLUTION FOUND AFTER {hilltries} hillclimbs, IT TOOK {wire_count + len(all_sets)} pieces of wire")

            return all_sets


        if len(new_unconnected_sets) < len(unconnected):

            for set in all_sets:
                if set.is_it_connected() == True:
                    pass

        else:
            for set in all_sets:
                set.disconnect()

            for set in all_sets:
                if set.was_it_connected() == True:
                    set.set_route(set.get_old_route())
                    set.reconnect()

    exit()

def hillimprove(max_tries, solved_sets):
    not_improved = 0
    best_so_far = len(solved_sets)
    for set in solved_sets:
        for point in set.get_route():
            if point.get_attribute() == "wire":
                best_so_far += 1
    print(f"STARTING HILLIMPROVE WITH {best_so_far} pieces of wire")
    better_solutions = []
    hillimproves = 0
    while(not_improved < max_tries):
        hillimproves += 1

        # Save all OG routes
        if hillimproves == 1:

            old_routes = {}
            print("FIRST HILLSOLVE REMEMBERING ROUTES")
            for set in solved_sets:
                old_routes[set] = set.get_route()

        # Take 2 random sets and disconnect them
        broken_sets = []
        np.random.shuffle(solved_sets)
        for i in range(2):
            broken_sets.append(solved_sets[i])
            solved_sets[i].disconnect()

        # Try to solve again
        new_all_sets, new_connected_sets, new_unconnected_sets = connect(broken_sets)

        # Check if solved:
        if len(new_unconnected_sets) == 0:
            wire_count = len(solved_sets)
            for set in solved_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            # If better
            if wire_count < best_so_far:
                not_improved = 0
                print(f"Found a BETTER solution after {hillimproves} hillimproves which takes {wire_count} instead of {best_so_far}")
                best_so_far = wire_count

                # Save old routes again
                for set in solved_sets:
                    old_routes[set] = set.get_route()


            else:
                not_improved += 1

                for set in new_all_sets:
                    set.disconnect()
                    set.set_route(old_routes[set])
                    set.reconnect()

        # If no solution was found
        else:
            not_improved += 1
            for set in new_all_sets:
                set.disconnect()
                set.set_route(old_routes[set])
                set.reconnect()



def simulated_annealing(max_tries, solved_sets, allowance):
    not_improved = 0
    temp = 1
    T_min = 0.00001
    alpha = 0.99
    best_so_far = len(solved_sets)
    for set in solved_sets:
        for point in set.get_route():
            if point.get_attribute() == "wire":
                best_so_far += 1
    print(f"STARTING HILLIMPROVE WITH {best_so_far} pieces of wire")
    better_solutions = []
    hillimproves = 0
    while(not_improved < max_tries and temp > T_min):
        hillimproves += 1
        allowance -= 0.1

        # Save all OG routes
        if hillimproves == 1:

            old_routes = {}
            print("FIRST HILLSOLVE REMEMBERING ROUTES")
            for set in solved_sets:
                old_routes[set] = set.get_route()

        # Take 2 random sets and disconnect them
        broken_sets = []
        np.random.shuffle(solved_sets)
        for i in range(2):
            broken_sets.append(solved_sets[i])
            solved_sets[i].disconnect()

        # Try to solve again
        new_all_sets, new_connected_sets, new_unconnected_sets = connect(broken_sets)

        # Check if solved:
        if len(new_unconnected_sets) == 0:

            wire_count = len(solved_sets)
            for set in solved_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            # Calculate SA chance
            ap = acceptance_probability(best_so_far, wire_count, temp)

            # If better
            if wire_count < best_so_far:
                not_improved = 0
                print(f"Found a BETTER solution after {hillimproves} hillimproves which takes {wire_count} instead of {best_so_far}")
                best_so_far = wire_count

                # Save old routes again
                for set in solved_sets:
                    old_routes[set] = set.get_route()

            # If not better BUT continuing because of simulated annealing
            elif ap > random.random():
                not_improved = 0
                print(f"SIMULATED ANNEALING SAVED YOU. WORSE SOLUTION after {hillimproves} hillimproves which takes {wire_count} instead of {best_so_far}")
                best_so_far = wire_count

                # Save old routes again
                for set in solved_sets:
                    old_routes[set] = set.get_route()

            # If worse and too bad to continue with for simulated annealing
            else:
                print("***")
                print("NOT ACCEPTING THE NEW SOLUTION")
                print("***")
                not_improved += 1
                for set in new_all_sets:
                    set.disconnect()
                    set.set_route(old_routes[set])
                    set.reconnect()

        # If no solution was found
        else:
            not_improved += 1
            for set in new_all_sets:
                set.disconnect()
                set.set_route(old_routes[set])
                set.reconnect()

        temp *= alpha

    return None

def acceptance_probability(old_cost, new_cost, temp):
    ap = math.exp((old_cost-new_cost) / temp)
    return ap
