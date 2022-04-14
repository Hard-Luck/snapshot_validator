"""Script to take unformatted csv file and remove wallets with less that 1000 in all snapshots
and return new csv with {ADRESS: [snapshots]}"""

import csv

air_drop_balances = {}
# Open entire file and format into desired dict
with open(
    "./static/Phore Snapshots - Graphene Airdrops - Snapshots - All.csv"
) as snapshot_file:
    balances = csv.DictReader(snapshot_file)
    for row in balances:
        air_drop_balances[row["PHR Address"]] = [
            row["Snapshot 1"],
            row["Snapshot 2"],
            row["Snapshot 3"],
            row["Snapshot 4"],
            row["Snapshot 5"],
            row["Snapshot 6"],
        ]

# Initialize new dict to enter only where balance ever exceeds 1000
relevant = {}

for wallet, values in air_drop_balances.items():
    # Skip if not valid
    if (
        float(values[0]) < 1000
        and float(values[1]) < 1000
        and float(values[2]) < 1000
        and float(values[3]) < 1000
        and float(values[4]) < 1000
        and float(values[5]) < 1000
    ):
        continue
    # Enter into new dict
    else:
        relevant[wallet] = values

# Write CSV file to disk
with open("./static/min_1000(1).csv", "w") as f:
    for key in relevant.keys():
        value = relevant[key]
        f.write(f"{key}," + ", ".join(str(x) for x in value) + "\n")
