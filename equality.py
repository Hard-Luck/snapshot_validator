import csv
import sys
from audioop import add

sys.stdout = open("log.txt", "w")

my_balances = {}
test_balances = {}

with open("balances_check.csv") as balances:
    reader = csv.reader(balances)
    for row in reader:
        my_balances[row[0]] = [float(x) for x in row[1:7]]

with open("static/min_1000(1).csv") as min1000:
    reader = csv.reader(min1000)
    for row in reader:
        test_balances[row[0]] = [float(x) for x in row[1:7]]

print("Address\t\t\t\t\t\t\t\t|\tSnapshot\t|\t\tMy calc\t\t\t|\tCurrent calc")
print(
    "------------------------------------------------------------------------------------------------"
)
for address, snapshots in my_balances.items():
    for index, snapshot in enumerate(snapshots):
        if snapshot == test_balances[address][index]:
            continue
        else:
            print(
                f"{address}\t|\t\t {index + 1}\t\t|\t{snapshot:.8f}\t\t|\t{test_balances[address][index]:.8f}"
            )
print(
    "\n\nNote: Most errors are due to multiple transactions in a block so multiple totals... "
)
sys.stdout.close()
