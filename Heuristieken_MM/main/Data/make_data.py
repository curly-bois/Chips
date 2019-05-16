import pandas as pd
from Classes.point import Point
from Classes.set import Set

def make_xlsx(all_sets,matrix,netlistname):

    wires = []
    order = []
    directions = []
    lower_bound = 0

    # get the data
    for set in all_sets:
        route = set.get_route()
        start = set.get_startpoint().get_id()
        end = set.get_endpoint().get_id()
        lower_bound += set.get_distance()
        directions.append(set.get_direction())
        wires.append(set.get_endpoint())

        order.append((start,end))
        for point in route:
            wires.append(point)

    count = 0

    #  get the upper bound
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            count += 1
            for k in range(len(matrix[i][j])):
                count += 1
    count *= len(matrix)

    # print(f"order = {order}")
    # print(f"directions of order = {directions}")
    print(f"upper bound = {count}")
    print(f"lower bound = {lower_bound}")
    print(f"amount of wires = {len(wires)}")


    # colums in the xlsx file
    data = {'netlist':netlistname}
    data['order'] = [order]
    data['directions of order'] = [directions]
    data['upper bound'] = count
    data['lower bound'] = lower_bound
    data['amount of wires'] = len(wires)

    output('Test.xlsx', data)


def output(filename, data):
    df = pd.read_excel(filename, sheet_name=0)
    df_new = pd.DataFrame(data, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.set_index('netlist', inplace=True)
    df_file.to_excel(filename)
