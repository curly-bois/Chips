# import xlsxwriter module
import xlsxwriter


def make_data(row,orderlist,not_connected):
# Start from the first cell.
# Rows and columns are zero indexed.
    xbook = xlsxwriter.Workbook('Test.xlsx')
    xsheet = xbook.add_worksheet('Test')
    # write operation perform
    xsheet.write(row,0,"orderlist")


    column = 1
    for i in orderlist:
        xsheet.write(row,column,i)
        column = column + 1

    column = 1
    row = row + 1
    xsheet.write(row,0,"not connnected")
    for i in not_connected:
        xsheet.write(row,column,i)
        column = column + 1

    # for i in not_connected:
    #     worksheet.write_string(row, 1, i)
    xbook.close()
