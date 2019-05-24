#  this sets the heuristicts off 
def dynamic(matrix):
    for three_dimensions in matrix:
        for two_dimensions in three_dimensions:
            for point in two_dimensions:
                point.set_dynamic(True)
