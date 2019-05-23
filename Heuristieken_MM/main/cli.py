
preprocessing = False
choices = []
heuristics = {1: ["normal A*-algorithm", 1],
              2: ["optimal routing (A-algorithm)", 1],
              3: ["order gates by direction", 2],
              4: ["order gates by amount of appearences", 2],
              5: ["order gates by random", 2],
              6: ["hill climber",3],
              7: ["simulated annealing",3],
              8: ["visualisation on a 3d grid"],
              9: ["save the end result in an excel file"],
              10: ["done selecting"],
              11: ["quit"]
             }
while True:


    print("Please select the number for the heuristics/algorithms/options you want to use for preprocessing:")
    print()

    for k, v in heuristics.items():
        print(f"({k})--{v[0]}")

    awnser = input("> ")

    awnser = int(awnser)

    if awnser == 11:
        exit()
    elif awnser == 10:
        break
    elif awnser in heuristics:
        choices.append(awnser)

    delete = []
    for choice in heuristics:
        try:
            if heuristics[choice][1] == heuristics[awnser][1]:
                delete.append(choice)
        except:
            pass
    del heuristics[awnser]
    for i in delete:
        del heuristics[i]

    if len(heuristics) <= 2:
        break
print(choices)
