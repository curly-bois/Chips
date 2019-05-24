import numpy as np
from Algorithms.connect import connect
import random
import math
from Preprocessing.init import *


def hillimprove(max_tries, solved_sets):
    current_try = 0

    # Get the current best score
    best_so_far = len(solved_sets)
    for set in solved_sets:
        for point in set.get_route():
            if point.get_attribute() == "wire":
                best_so_far += 1

    while(current_try < max_tries):

        # Save all OG routes
        if current_try == 0:
            old_routes = {}
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
        current_try += 1

        # Check if solved:
        if len(new_unconnected_sets) == 0:
            wire_count = len(solved_sets)
            for set in solved_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            # If better, go on with this state
            if wire_count < best_so_far:
                best_so_far = wire_count

                # Save old routes again
                for set in solved_sets:
                    old_routes[set] = set.get_route()

            # If the solution is equal or worse, go back to the previous state
            else:
                for set in new_all_sets:
                    set.disconnect()
                for set in solved_sets:
                    set.set_route(old_routes[set])
                for set in solved_sets:
                    set.reconnect()

        # If no solution was found, go back to the previous state
        else:
            for set in new_all_sets:
                set.disconnect()
            for set in solved_sets:
                set.set_route(old_routes[set])
            for set in solved_sets:
                set.reconnect()


def simulated_annealing(max_tries, solved_sets):
    current_try = 0
    temp = 1
    T_min = 0.00001
    alpha = 0.99

    # Calculate current score
    best_so_far = len(solved_sets)
    for set in solved_sets:
        for point in set.get_route():
            if point.get_attribute() == "wire":
                best_so_far += 1

    while(current_try < max_tries):

        # Save all OG routes
        if current_try == 0:
            old_routes = {}
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
        current_try += 1

        # Check if solved:
        if len(new_unconnected_sets) == 0:

            wire_count = len(solved_sets)
            for set in solved_sets:
                for point in set.get_route():
                    if point.get_attribute() == "wire":
                        wire_count += 1

            # If better
            if wire_count < best_so_far:
                best_so_far = wire_count

                # Save old routes again
                for set in solved_sets:
                    old_routes[set] = set.get_route()

            # If new solution is not better
            else:

                # Calculate SA chance
                ap = acceptance_probability(best_so_far, wire_count, temp)

                # If not better BUT continuing because of simulated annealing
                if ap > random.random():
                    best_so_far = wire_count

                    # Save old routes again
                    for set in solved_sets:
                        old_routes[set] = set.get_route()

                # If worse and too bad to continue with for simulated annealing
                else:
                    for set in new_all_sets:
                        set.disconnect()
                    for set in solved_sets:
                        set.set_route(old_routes[set])
                    for set in solved_sets:
                        set.reconnect()

        # If no solution was found
        else:
            for set in new_all_sets:
                set.disconnect()
            for set in solved_sets:
                set.set_route(old_routes[set])
            for set in solved_sets:
                set.reconnect()

        # Update the temperature
        temp *= alpha
    return None


def simulsolve(max_tries, all_sets, connected_sets, unconnected_sets, matrix):
    current_try = 0
    to_break = 1
    break_check = 0
    best_so_far = len(unconnected_sets)
    start_score = len(unconnected_sets)

    while(current_try < max_tries):

        # Break one more wire if after 100 tries no better solution was found
        if break_check == 100 and not (to_break > 3):
            break_check = 0
            to_break += 1

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
        if current_try == 0:
            old_routes = {}
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

        # Return all sets when solved
        if len(new_unconnected_sets) == 0:
            return all_sets

        # If not yet solved check if this is a better solution that we will accept
        new_score = 0
        for set in all_sets:
            if set.is_it_connected() == False:
                new_score += 1

        # If better or equal
        if best_so_far >= new_score:
            if best_so_far == new_score:
                break_check += 1
            else:
                break_check = 0
                to_break = 1
                current_try = 0

            # Update the best score so far
            best_so_far = new_score

            # Save old routes again
            for set in all_sets:
                old_routes[set] = set.get_route()

        # If not better, go back to previous state
        else:
            current_try += 1
            for set in new_all_sets:
                set.disconnect()
            for set in all_sets:
                set.set_route(old_routes[set])
            for set in initially_unconnected_sets:
                set.disconnect()
            for set in connected_sets:
                set.set_route(old_routes[set])
                set.reconnect()

    # Returns none when no solution has been found
    return None


def acceptance_probability(old_cost, new_cost, temp):

    # Calculates the acceptance probability
    ap = math.exp((old_cost-new_cost) / temp)
    return ap
