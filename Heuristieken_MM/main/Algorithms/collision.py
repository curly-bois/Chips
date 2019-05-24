def collision_check(all_sets):
    all_coordinates = []
    collisions = 0
    for set in all_sets:
        for routepoint in set.get_route():
            all_coordinates.append(routepoint.get_location())

    for i in all_coordinates:
        if all_coordinates.count(i) > 1:
            collisions += 1

    return collisions
