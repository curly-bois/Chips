import pandas as pd
from Classes.point import Point
from Classes.set import Set

def make_xlsx(all_sets,matrix,netlistname,collisions,method):

    order = []
    directions = []
    lower_bound = 0
    unconnected_sets = []

    # get the wire pieces for the length
    wire_pieces = len(all_sets)
    for three_dimensions in matrix:
        for two_dimensions in three_dimensions:
            for point in two_dimensions:
                if point.get_attribute() == "wire":
                    wire_pieces += 1

    # get the data from connected and unconnected sets
    for set in all_sets:
        if not set.is_it_connected():
            unconnected_sets.append(set)
        start = set.get_startpoint().get_id()
        end = set.get_endpoint().get_id()
        order.append((start,end))
        lower_bound += set.get_distance()
        directions.append(set.get_direction())


    #  get the upper bound
    height = len(matrix)
    width = len(matrix[0])
    length = len(matrix[0][0])

    upper_bound = (length * width * height)


    # colums in the xlsx file
    data = {'netlist':netlistname}
    data['order'] = [order]
    data['directions of order'] = [directions]
    data['upper bound'] = upper_bound
    data['lower bound'] = lower_bound
    data['amount of wires'] = wire_pieces
    data['unconnected'] = f"{int(len(unconnected_sets) / len(all_sets) * 100)}%"
    data['collisions'] = collisions
    data['method'] = method

    # Write to the excel file
    output('test.xlsx', data)


def output(filename, data):
    df = pd.read_excel(filename, sheet_name=0)
    df_new = pd.DataFrame(data, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.set_index('netlist', inplace=True)
    df_file.to_excel(filename)

def print_data(all_sets,matrix,netlistname,collisions,method):
    order = []
    directions = []
    lower_bound = 0
    unconnected_sets = []

    # get the wire pieces for the length
    wire_pieces = len(all_sets)
    for three_dimensions in matrix:
        for two_dimensions in three_dimensions:
            for point in two_dimensions:
                if point.get_attribute() == "wire":
                    wire_pieces += 1

    # get the data from connected and unconnected sets
    for set in all_sets:
        if not set.is_it_connected():
            unconnected_sets.append(set)
        start = set.get_startpoint().get_id()
        end = set.get_endpoint().get_id()
        order.append((start,end))
        lower_bound += set.get_distance()
        directions.append(set.get_direction())


    #  get the upper bound
    height = len(matrix)
    width = len(matrix[0])
    length = len(matrix[0][0])

    upper_bound = (length * width * height)

    print(f"{netlistname} has been run with {int(len(unconnected_sets) / len(all_sets) * 100)}% unconnected sets")
    print(f"the lower bound was {lower_bound} and the upper bound was {upper_bound} amount of wire pieces")
    print(f"{wire_pieces} wire pieces where used to connect the gates")
    print(f"there where {collisions} collisions")
