import re

def get_grid(txt):
    # read the .txt file
    with open(txt, "r") as f:
        # filter only things inbetween brackets
        text = re.findall('\(.*?\)',f.read())

    highX = 0
    highY = 0
    grid = []
    for number in text:
        number = number.replace(")", "")
        number = number.replace("(", "")
        number = number.split(",")
        x = int(number[0])
        y = int(number[1])
        tuplist = [x,y]
        grid.append(tuple(tuplist))
        if x > highX:
            highX = x
        if y > highY:
            highY = y

    return grid, max(highX,highY)+2
