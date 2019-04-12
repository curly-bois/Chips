import csv

with open('print_1.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        print(row)

points = {}
# read the csv file and make it a dictionary
with open('print_1.csv', fieldnames= ["No","x","y"]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
