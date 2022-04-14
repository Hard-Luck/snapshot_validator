import os

import numpy as np
import pandas as pd

# Block Heights
snapshots = [
    "1817125",
    "1856572",
    "1896008",
    "1935435",
    "1971468",
    "1999951",
]


def format_csv(file: str) -> pd.DataFrame:
    """Remove first line and uneccesary colums from explorer data"""

    df = pd.read_csv(file, sep=";", skiprows=1)
    df = df.drop(labels="Transaction", axis=1)
    df = df.drop(labels="Type", axis=1)
    df = df.drop(labels="Amount", axis=1)
    return df


def insert_blocks(block: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    """Insert snapshot blocks into df with 0 values as a reference point"""

    # Check that block doesn't already exist in df
    if (dataframe["Block"] != block).any():
        pd.DataFrame([[block, 0, 0]], columns=["Block", "Data/Time", "Total"])
        # insert proxy values
        dataframe.loc[len(dataframe.index)] = [block, 0, "Test_Block"]

    else:
        print("block exists")
    return dataframe


def get_index(blocks: list[str], dataframe: pd.DataFrame) -> list[int]:
    """Get the index of the dummy blocks that were inserted"""
    indices = []
    for block in blocks:
        indices.append(np.flatnonzero(dataframe["Block"] == int(block))[0])
    return indices


def get_balances(block_heights: list[int], dataframe: pd.DataFrame) -> list:
    """Check the transaction before the index to see what the balance was"""
    # Initialise empty list for snapshot balance
    snapshot_balances = []
    balance_index = [x - 1 for x in block_heights]
    rows = dataframe.shape[0]
    # Ensure if dummy value is first "transaction" snapshot value is 0
    while rows in balance_index:
        snapshot_balances.append(0)

    # Append the balance immediately before the snapshot
    value = list(dataframe["Total"].iloc[balance_index])
    snapshot_balances = snapshot_balances + value
    return snapshot_balances


def fix_dummy(balances: list) -> list[float]:
    """Fix the dummy values picked up by making them equal to most recent real value
    or zero if dummy transaction is first recoded"""
    for index, balance in enumerate(balances):
        if index == 0 and balance == "Test_Block":
            balances[index] = 0
            continue
        elif balance == "Test_Block":
            balances[index] = balances[index - 1]
    return balances


def main():
    for filename in os.listdir("CSV_files"):
        df = format_csv(f"CSV_files/{filename}")
        address = filename.replace(".csv", "")
        # Insert all the reference block heights
        for snapshot in snapshots:
            insert_blocks(snapshot, df)

        # Change blocks from string to numeric
        df["Block"] = df["Block"].apply(pd.to_numeric)

        # Sort the dataframe by blocks
        df = df.sort_values("Block", ignore_index=True, ascending=True)

        block_height = get_index(snapshots, df)
        balances = get_balances(block_height, df)
        balances = fix_dummy(balances)

        with open("balances_check.csv", "a") as fd:
            fd.write(f"{address}, " + ", ".join(str(x) for x in balances) + "\n")


if __name__ == "__main__":
    main()
