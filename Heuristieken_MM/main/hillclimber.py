import numpy as np
from connect import connect
import random
import math

def hillsolve(max_tries, matrix, all_sets, unconnected_sets, connected_sets):
    hilltries = 0
    while len(unconnected_sets) > 0 and hilltries < max_tries:
        hilltries += 1
        if hilltries == 1:

            old_routes = {}
            for set in all_sets:
                print("FIRST HILLTRY REMEMBERING ROUTES")
                old_routes[set] = set.get_route()

        np.random.shuffle(connected_sets)

        new_connections = []
        broken_sets = []

        for set in unconnected_sets:
            new_connections.append(set)
            # print(f"These are the unconnected sets in try {hilltries}: {set}, and this set is {set.is_it_connected()}")

        sets_to_be_broken = int(len(connected_sets) * 0.2)
        for i in range(sets_to_be_broken):
            connected_sets[i].disconnect()
            new_connections.append(connected_sets[i])
            broken_sets.append(connected_sets[i])
            # print(f"These sets are being broken now in try {hilltries}:  {connected_sets[i]}, this set is {set.is_it_connected()} ")

        new_all_sets, new_connected_sets, new_unconnected_sets = connect(new_connections)

        print(f"After this {int(len(new_unconnected_sets) / len(all_sets) * 100)}% is unconnected")
        if len(new_unconnected_sets) == 0:
            wire_pieces = 0
            for three_dimensions in matrix:
                for two_dimensions in three_dimensions:
                    for point in two_dimensions:
                        if point.get_attribute() == "wire":
                            wire_pieces += 1
            print(f"SOLUTION HAS BEEN FOUND after {hilltries} hillclimbs, IT TOOK {wire_pieces + len(all_sets)} pieces of wire")

            wire_count = 0
            for set in all_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            print(f"ALTERNATIVE COUNT, SOLUTION FOUND AFTER {hilltries} hillclimbs, IT TOOK {wire_count + len(all_sets)} pieces of wire")

            return all_sets

        for set in new_all_sets:
            # print(f"These sets are being disconnected now in try {hilltries}:  {set}, this set is {set.is_it_connected()} ")
            set.disconnect()

        for set in all_sets:
            set.set_route(old_routes[set])

        for set in unconnected_sets:
            set.set_route(old_routes[set])
            set.disconnect()

        for set in connected_sets:
            set.set_route(old_routes[set])
            # print(f"These sets are being reconnected now in try {hilltries}:  {set}, this set is {set.is_it_connected()} ")
            set.reconnect()


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

    # Calculate current score
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
                print(f"Found a BETTER solution after {hillimproves} hillimproves which takes {wire_count} wires pieces instead of {best_so_far}")
                best_so_far = wire_count

                # Save old routes again
                for set in new_all_sets:
                    old_routes[set] = set.get_route()

            # If not better BUT continuing because of simulated annealing
            elif ap > random.random():
                not_improved = 0
                print(f"SIMULATED ANNEALING SAVED YOU. WORSE SOLUTION after {hillimproves} hillimproves which takes {wire_count} wire pieces instead of {best_so_far}")
                best_so_far = wire_count

                # Save old routes again
                for set in new_all_sets:
                    old_routes[set] = set.get_route()

            # If worse and too bad to continue with for simulated annealing
            else:
                print("***")
                print("NOT ACCEPTING THE NEW SOLUTION")
                print("***")
                not_improved += 1
                # !!! dit slaat nergens op
                for set in new_all_sets:
                    set.disconnect()
                    set.set_route(old_routes[set])
                    set.reconnect()

        # If no solution was found
        else:
            not_improved += 1
            # !!! dit slaat nergens op
            for set in new_all_sets:
                set.disconnect()
                set.set_route(old_routes[set])
                set.reconnect()

        temp *= alpha

    return None


def simulsolve(max_tries, all_sets, connected_sets, unconnected_sets):
    not_improved = 0
    temp = 1
    T_min = 0.00001
    alpha = 0.99
    to_break = 1
    break_check = 0
    best_so_far = len(unconnected_sets)
    start_score = len(unconnected_sets)
    print(f"STARTING SIMULSOLVE WITH {best_so_far} solved sets")
    better_solutions = []
    hillimproves = 0
    while(not_improved < max_tries):
        if break_check == 100 and not (to_break > 5):
            break_check = 0
            to_break += 1
        hillimproves += 1

        # Create new list for new tries
        new_tries = []
        initially_unconnected_sets = []
        connected_sets = []
        for set in all_sets:
            if set.is_it_connected() == False:
                initially_unconnected_sets.append(set)
                new_tries.append(set)
            else:
                connected_sets.append(set)

        # Save all OG routes in first iteration
        if hillimproves == 1:
            old_routes = {}
            print("FIRST HILLSOLVE REMEMBERING ROUTES")
            for set in all_sets:
                old_routes[set] = set.get_route()

        # Break a random set
        broken_sets = []
        np.random.shuffle(connected_sets)
        for i in range(to_break):
            connected_sets[i].disconnect()
            broken_sets.append(connected_sets[i])
            new_tries.append(connected_sets[i])

        # Try to solve again
        np.random.shuffle(new_tries)
        new_all_sets, new_connected_sets, new_unconnected_sets = connect(new_tries)

        # Check if solved:
        if len(new_unconnected_sets) == 0:
            print(f"SIMULSOLVE FOUND A SOLUTION AFTER {hillimproves} simulsolves")
            return all_sets

        # If not yet solved check if this is a better solution that we will accept
        new_score = 0
        for set in all_sets:
            if set.is_it_connected() == False:
                new_score += 1

        # Calculate SA chance
        # ap = acceptance_probability(best_so_far, new_score, temp)

        # If better
        if best_so_far >= new_score:
            if best_so_far == new_score:
                break_check += 1
            else:
                break_check = 0
                to_break = 1
            not_improved = 0
            print(f"Found a BETTER solution after {hillimproves} hillimproves with {new_score} unconnected sets instead of {best_so_far}")
            best_so_far = new_score

            # Save old routes again
            for set in all_sets:
                old_routes[set] = set.get_route()

        # If not better BUT continuing because of simulated annealing
        # elif ap > random.random():
        #     not_improved = 0
        #     print(f"SIMULATED ANNEALING SAVED YOU. WORSE SOLUTION after {hillimproves} hillimproves with {new_score} unconnected sets instead of {best_so_far}")
        #     best_so_far = new_score
        #
        #     # Save old routes again
        #     for set in all_sets:
        #         old_routes[set] = set.get_route()

        # If worse and too bad to continue with for simulated annealing
        else:
            print("***")
            print("NOT ACCEPTING THE NEW SOLUTION")
            print("***")
            not_improved += 1

            for set in new_all_sets:
                set.disconnect()

            for set in all_sets:
                set.set_route(old_routes[set])

            for set in initially_unconnected_sets:
                set.disconnect()

            for set in connected_sets:
                set.set_route(old_routes[set])
                set.reconnect()


            # for set in new_all_sets:
            #     # print(f"These sets are being disconnected now in try {hilltries}:  {set}, this set is {set.is_it_connected()} ")
            #     set.disconnect()
            #
            # for set in all_sets:
            #     set.set_route(old_routes[set])
            #
            # for set in unconnected_sets:
            #     set.set_route(old_routes[set])
            #     set.disconnect()
            #
            # for set in connected_sets:
            #     set.set_route(old_routes[set])
            #     # print(f"These sets are being reconnected now in try {hilltries}:  {set}, this set is {set.is_it_connected()} ")
            #     set.reconnect()


        temp *= alpha

    # Returns none when no solution has been found
    print(f"simulsolve did not find a solution after {hillimproves} simulsolves, the amount of sets connected at the start was {start_score} and now it is {best_so_far}")
    return None

def acceptance_probability(old_cost, new_cost, temp):
    ap = math.exp((old_cost-new_cost) / temp)
    return ap
