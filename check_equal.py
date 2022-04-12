import csv
from audioop import add

my_balances = {}
test_balances = {}

with open("balances_check.csv") as balances:
    reader = csv.reader(balances)
    for row in reader:
        my_balances[row[0]] = [float(x) for x in row[1:]]

with open("min_1000.csv") as min1000:
    reader = csv.reader(min1000)
    for row in reader:
        test_balances[row[0]] = [float(x) for x in row[1:]]

for address, snapshots in my_balances.items():
    for index, snapshot in enumerate(snapshots):
        if snapshot == test_balances[address][index]:
            print("True")
        else:
            print("False")
