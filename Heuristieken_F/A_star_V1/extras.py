def dis(s,e,m):
    dis = abs(s[0]-5)+abs(s[1]-5)+abs(e[0]-5)+abs(e[1]-5)
    return dis

def sort_points(starts, ends):
    distance = [dis(s,e,5) for s,e in zip(starts,ends)]
    index = [dis(s,e,5) for s,e in zip(starts,ends)]
    distance.sort()

    points_unsorted = list(zip(starts,ends))

    points = []
    for item in distance:
        i = index.index(item)
        points.append(points_unsorted[i])
        index[i] = -1

    return points
