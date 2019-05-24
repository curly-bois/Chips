
def menu():

    A_star = {1: "normal A*-algorithm",
              2: "optimal routing (A-algorithm)",
              3: "quit"
             }

    order = {1: "order gates by direction",
             2: "order gates by amount of appearences",
             3: "order gates by random",
             4: "quit"
            }

    iterative = { 1: "hill climber",
                  2: "simulated annealing",
                  3: "none",
                  4: "quit"
                 }

    optiondict = {1: "visualisation on a 3d grid",
               2: "save the end result in an excel file",
               3: "done selecting",
               4: "quit"
               }

    print("select your way of pathfinding")
    for k, v in A_star.items():
        print(f"({k})--{v}")

    awnser = input("> ")
    awnser = int(awnser)
    if A_star[awnser] == "quit":
        exit()
    astarchoice = awnser

    print("select the order you want to make")
    for k, v in order.items():
        print(f"({k})--{v}")

    awnser = input("> ")
    awnser = int(awnser)
    if order[awnser] == "quit":
        exit()
    orderchoice = awnser

    print("select the iterative algorithm you want to use")
    for k, v in iterative.items():
        print(f"({k})--{v}")

    awnser = input("> ")
    awnser = int(awnser)
    if iterative[awnser] == "quit":
        exit()
    if iterative[awnser] != "none":
        iterchoice = awnser
    else:
        iterchoice = 0

    print("select other options")
    options = []
    while True:
        if len(optiondict) <= 2:
            break

        for k, v in optiondict.items():
            print(f"({k})--{v}")

        awnser = input("> ")
        awnser = int(awnser)
        if optiondict[awnser] == "done selecting":
            break
        if optiondict[awnser] == "quit":
            exit()
        options.append(awnser)
        del optiondict[awnser]

    print("select the netlist you want to use:")

    netlist = int(input(">"))

    if netlist <= 3:
        grid = 1
    elif netlist <=6:
        grid = 2
    else:
        print("netlist number must be inbetween 1 and 6")
        exit()

    print("select the amount of times you want to try it")

    tries = int(input(">"))

    return astarchoice, orderchoice,iterchoice, options,tries, netlist, grid
