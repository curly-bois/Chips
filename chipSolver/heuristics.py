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


def plant_prop_lite(generation, options):
    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    fifty_mark = float(options['half_prop'])

    delta_t = fifty_mark**(1/(loops/2))

    gen_len  = len(generation)
    swap_list = [ i+1 * swaps for i in range(gen_len)]
    temp_list = [ (i*(1/gen_len))+0.1 for i in range(gen_len)]

    for iter in range(int(loops/8)): #50

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):

            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]

            t = 1
            for i in range(loops): #100
                gen.main, new_wires , new_not_con = swap_wiresA_P(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            t*TEMP)

                new_wires = shuffle(new_wires)
                new_not_con = shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)

                t = update_temperature(t, delta_t)



    generation.sort(key=sortit)
    generation.reverse()

    shortest = generation[0].score1()

    short_list = []
    for gen in generation:
        if gen.score1() == shortest:
            short_list.append(gen)

    short_list.sort(key=shortestit)
    return short_list[0]

def sim_annealing(main, options):
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    fifty_mark = float(options['half_prop'])

    delta_t = fifty_mark**(1/(loops/2))

    print('Start loop 1')
    t = 1.00
    data = []
    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wiresA_P(Wires,
                                                    not_connected,
                                                    mainGrid,
                                                    swaps,
                                                    t)

        Wires = shuffle(Wires)
        data.append([sum([w.length for w in Wires]), len(Wires)])
        t = update_temperature(t, delta_t)

    print('Not crossing', Check(Wires))

    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main, data

def hill_climber(main, options):
    mainGrid = main.main
    Wires = main.gwires()
    not_connected = main.gnotc()

    loops = int(options['swaploops'])
    swaps = int(options['swaps'])

    data = []
    for i in range(loops):
        mainGrid, Wires, not_connected = swap_wires(Wires,
                                                    not_connected,
                                                    mainGrid,
                                                    swaps)

        Wires = shuffle(Wires)
        data.append([sum([w.length for w in Wires]), len(Wires)])

    print('Not crossing', Check(Wires))

    main.main = mainGrid
    main.swires(Wires)
    main.snotc(not_connected)

    return main, data

def plant_prop(generation, options, SIZE, all_points):

    loops = int(options['swaploops'])
    swaps = int(options['swaps'])
    iterations = int(options['generations'])
    fifty_mark = float(options['half_prop'])
    GENS = len(generation)

    delta_t = fifty_mark**(1/(loops/2))
    swap_list = [ i+1 * swaps for i in range(len(generation))]
    temp_list = [ (i*(1/len(generation)))+0.1 for i in range(len(generation))]

    for iter in range(iterations): #50

        scrore_board = [i.score1() for i in generation]
        scrore_board.sort()
        scrore_board.reverse()
        print(f'{iter}. Current scores:', scrore_board)


        for i, gen in enumerate(generation):
            SWAPS = swap_list[scrore_board.index(gen.score1())]
            TEMP = temp_list[scrore_board.index(gen.score1())]
            for i in range(loops): #100
                gen.main, new_wires , new_not_con = swap_wiresA_P(gen.gwires(),
                                                            gen.gnotc(),
                                                            gen.main,
                                                            SWAPS,
                                                            gen.t*TEMP)

                new_wires = shuffle(new_wires)
                new_not_con = shuffle(new_not_con)

                gen.snotc(new_not_con)
                gen.swires(new_wires)

                gen.t = update_temperature(gen.t, delta_t)



        generation.sort(key=sortit)
        generation.reverse()

        shortest = generation[0].score1()

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

    return X
