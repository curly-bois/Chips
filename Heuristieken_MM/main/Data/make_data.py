import pandas as pd
from Classes.point import Point
from Classes.set import Set

def make_xlsx(all_sets,connected_sets,matrix,netlistname,unconnected_sets):

    wires = []
    order = []
    directions = []
    lower_bound = 0

    # get the data form the connected sets (wire length only)
    for set in connected_sets:
        route = set.get_route()
        wires.append(set.get_endpoint())
        for point in route:
            wires.append(point)

    # get the data that has to do someting with all the sets
    for set in all_sets:
        start = set.get_startpoint().get_id()
        end = set.get_endpoint().get_id()
        order.append((start,end))
        lower_bound += set.get_distance()
        # directions.append(set.get_direction())

    #  get the upper bound
    height = len(matrix)
    width = len(matrix[0])
    length = len(matrix[0][0])

    upper_bound = (length * width * height)

    # print(f"order = {order}")
    # print(f"directions of order = {directions}")
    # print(f"upper bound = {count}")
    # print(f"lower bound = {lower_bound}")
    # print(f"amount of wires = {len(wires)}")
    # print(f"unconnected = {int(len(unconnected_sets) / len(all_sets) * 100)}")

    # colums in the xlsx file
    data = {'netlist':netlistname}
    data['order'] = [order]
    data['directions of order'] = [directions]
    data['upper bound'] = upper_bound
    data['lower bound'] = lower_bound
    data['amount of wires'] = len(wires)
    data['unconnected'] = f"{int(len(unconnected_sets) / len(all_sets) * 100)}%"

    output('test.xlsx', data)


def output(filename, data):
    df = pd.read_excel(filename, sheet_name=0)
    df_new = pd.DataFrame(data, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.set_index('netlist', inplace=True)
    df_file.to_excel(filename)
