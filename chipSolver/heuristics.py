from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *
from data import get_data
from instance import Instance

import random
import time
import pickle

import os
import sys
import copy


def sim_annealing(generation, options, SIZE, all_points, tpnum):
    '''
    Simulated Annealing
    '''
    # Make single instance
    main = generation[0]
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    # Get vars
    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    delta_t = 0.01**(1/loops)

    t = 1.00
    data = []
    for i in range(loops):
        # Print current loop
        loading(i, loops, len(Wires))

        # swap x wires, accept better results or worse on probability
        mainGrid, Wires, not_connected = swap_wires_prop(Wires,
                                                        not_connected,
                                                        mainGrid,
                                                        swaps,
                                                        t)

        # Append score to data and shuffle wires for more randomness
        random.shuffle(Wires)
        data.append([sum([w.length for w in Wires]), len(Wires)])

        # Update temprature
        t = update_temperature(t, delta_t)

    # Return instance
    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main, data

def hill_climber(generation, options, SIZE, all_points, tpnum):
    '''
    Hill climber
    '''
    # Make single instance
    main = generation[0]
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    # Get vars
    loops = int(options['swaploops'])
    swaps = int(options['swaps'])

    data = []
    for i in range(loops):
        # Print current loop
        loading(i, loops, len(Wires))

        # swap x wires, accept only better results
        mainGrid, Wires, not_connected = swap_wires(Wires,
                                                    not_connected,
                                                    mainGrid,
                                                    swaps)

        # Append score to data and shuffle wires for more randomness
        random.shuffle(Wires)
        data.append([sum([w.length for w in Wires]), len(Wires)])

    # Return instance
    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main, data

def plant_prop(generation, options, SIZE, all_points, tpnum):
    '''
    Classic plant propegation
    '''
    # Set some vars
    loops = int(options['swaploops'])
    GENS = len(generation)
    MAX = int(tpnum)

    data = []
    for iter in range(loops):
        # Make new childs/ runners
        for i, gen in enumerate(generation):
            random.shuffle(gen.wires)
            gen.main, new_wires , new_not_con = swap_wires_plant(gen.gwires(),
                                                        gen.gnotc(),
                                                        gen.main,
                                                        gen.swap)

            random.shuffle(new_not_con)
            gen.snotc(new_not_con)
            gen.swires(new_wires)

        # Sort on score
        generation.sort(key=sortbothvalue, reverse=True)
        s1 = generation[0].score1()
        s2 = generation[0].score2()

        # Save data and show current
        data.append((s2,s1))
        print(f'{iter}. Current best:' ,s1 ,'len:' ,s2, end='\r')

        # Choose new gens
        generation.sort(key=sortbothvalue, reverse=True)
        generation_score = [sortbothvalue(i) for i in generation[:GENS]]

        # Get max and min
        ma = max(generation_score)
        mi = min(generation_score)

        # Avoid devision by zero
        if mi-ma == 0:
            ma += 0.0000001

        # Make new childs
        new_gen = []
        for i, gen in enumerate(generation[:GENS]):
            score = cal_fitness(ma, mi, gen)
            # Adjust for score
            generation1 = make_new_gen(gen,
                                       repo_s(score),
                                       swap_s(score, MAX),
                                       SIZE,
                                       all_points)
            new_gen += generation1 # push list to list

        del generation
        generation = new_gen

    return generation[0], data


### Experimental, slow
def plant_prop_sima(generation, options, SIZE, all_points, tpnum):
    '''
    Plant prop like function with temprature
    '''

    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    iterations = int(options['generations'])
    fifty_mark = float(options['half_prop'])
    GENS = len(generation)

    delta_t = fifty_mark**(1/(loops/2))
    swap_list = [ i+1 * swaps for i in range(len(generation))]
    temp_list = [ (i*(1/len(generation)))+0.1 for i in range(len(generation))]

    data = []

    for iter in range(iterations): #50

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):
            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]
            for i in range(loops): #100
                gen.main, new_wires , new_not_con = swap_wires_prop(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            gen.t*TEMP)

                random.shuffle(new_wires)
                random.shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)
                gen.t = update_temperature(gen.t, delta_t)

        generation.sort(key=sortit)
        generation.reverse()

        shortest = generation[0].score1()
        data.append([sum([w.length for w in generation[0].wires]),
                    len(generation[0].wires)])

        short_list = []
        for gen in generation:
            if gen.score1() == shortest:
                short_list.append(gen)

        short_list.sort(key=shortestit)
        X = short_list[0]

        generation = [Instance(Grid(SIZE, all_points)) for i in range(GENS)]
        for geni in generation:
            geni.snotc([i for i in X.not_connected])
            new_wire = []
            for i,w in enumerate(X.wires):
                new_wire.append(Wire(w.start, w.end, w.route))
                geni.main.add_wire(new_wire[i])
            geni.swires(new_wire)

    return X, data

def local_sima(generation, options, SIZE, all_points, tpnum):
    '''
    Local search with simulated annealing
    '''
    # Get variables
    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    fifty_mark = float(options['half_prop'])
    delta_t = 0.01**(1/(loops))

    # Make the division of temp and swaps
    gen_len  = len(generation)
    swap_list = [ i+1 * swaps for i in range(gen_len)]
    temp_list = [ (i*(1/gen_len))+0.1 for i in range(gen_len)]

    data = []
    for iter in range(int(loops/4)): #Random part of the loops

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):

            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]

            t = 1
            for i in range(loops): #100
                gen.main, new_wires , new_not_con = swap_wires_prop(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            t*TEMP)

                random.shuffle(new_wires)
                random.shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)

                t = update_temperature(t, delta_t)

    generation.sort(key=sortit)
    generation.reverse()

    shortest = generation[0].score1()
    data.append([sum([w.length for w in generation[0].wires]),
                len(generation[0].wires)])

    short_list = []
    for gen in generation:
        if gen.score1() == shortest:
            short_list.append(gen)

    short_list.sort(key=shortestit)
    return short_list[0], data
