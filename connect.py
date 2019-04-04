
import load

def main(txt):
    # Make grid
    points, size_grid = load.get_grid(txt)

    grid = [[True for i in range(size_grid)] for i in range(size_grid)]
    x, y = zip(*points)

    for p in points:
        grid[p[0]][p[1]] = False


    # Clear lines
    lines = []

    # Choose first point
    maxi = [sum(i) for i in points]
    index = maxi.index(min(maxi))

    # First point and end point
    xstart = points[index][0]
    ystart = points[index][1]

    pop_points = points
    pop_points.pop(index)
    distance = [abs(i[0]-xstart)+abs(i[1]-ystart) for i in pop_points]
    closest_point = pop_points[distance.index(min(distance))]

    # Setup loop
    first = True
    a_points = pop_points
    # grid_false = points

    # Loop until empty
    while len(a_points) > 0:

        if first:
            cur = (xstart, ystart)
            line = [cur]
            end = closest_point
            first = False
        else:
    #         a_points = points
            a_points.pop(a_points.index(end))
            if not a_points == []:
                distance = [abs(i[0]-end[0])+abs(i[1]-end[1]) for i in a_points]
                closest_point = a_points[distance.index(min(distance))]
                cur = end
                end = closest_point
            else:
                cur = end
                end = (xstart, ystart)
            line = [cur]


        while True:
            pos = [(cur[0]+1,cur[1]),
                   (cur[0]-1,cur[1]),
                   (cur[0],cur[1]+1),
                   (cur[0],cur[1]-1)]

            if end in pos:
                line.append(end)
                print("LINE FOUND")
                break

            fail = []
            for i,p in enumerate(pos):
                try:
                    if not grid[p[0]][p[1]]:
                        fail.append(i)
    #                 if p[0] < 0 or p[1] < 0:
    #                     fail.append(i)
                except:
                    fail.append(i)


            good_pos = [pos[i] for i in range(len(pos)) if not i in fail]
            pos = good_pos

            distance = [abs(i[0]-end[0])+abs(i[1]-end[1]) for i in pos]
            try:
                c_p = pos[distance.index(min(distance))]
            except:
                print(f"no combinations at line: {line}")
                break

            grid[c_p[0]][c_p[1]] = False

            line.append((c_p))
            cur = c_p


        lines.append(line)
    return lines
