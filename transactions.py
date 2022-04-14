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


class Transactions:
    """Class that handles all transactional behaviours"""

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.df: pd.DataFrame = pd.read_csv(self.filename, sep=";", skiprows=1)

    def format_csv(self):
        """Remove first line and uneccesary colums from explorer data"""
        self.df.drop(labels="Transaction", axis=1, inplace=True)
        self.df.drop(labels="Type", axis=1, inplace=True)
        self.df.drop(labels="Amount", axis=1, inplace=True)

    def insert_block(self, block: str):
        """Insert snapshot blocks into df with 0 values as a reference point"""
        # Check that block doesn't already exist in df
        if (self.df["Block"] != block).any():
            self.df([[block, 0, 0]], columns=["Block", "Data/Time", "Total"])
            # insert proxy values
            self.df.loc[len(self.df.index)] = [block, 0, "Test_Block"]
        else:
            print("block exists")

    def get_index(self, block: str) -> str:
        """Get the index of the dummy blocks that were inserted"""
        return np.flatnonzero(self.df["Block"] == int(block))[0]


def get_balances(block_heights: list[int], dataframe: pd.DataFrame) -> list:
    """Check the transaction before the index to see what the balance was"""
    # Initialise empty list for snapshot balances
    num_rows = dataframe.shape[0] - 1
    balances = []
    # Check if snapshot 1 would be first entry(last index)
    if num_rows in block_heights:
        block_heights.remove(num_rows)
        balances.append(0)
    # Append the balance immediately before the snapshot
    block_heights = [x + 1 for x in block_heights]
    value = list(dataframe["Total"].iloc[(block_heights)])
    balances.insert(0, [x for x in value])
    # Fix all values not affected by transactions

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
        df = df.sort_values("Block", axis=0, ignore_index=True, ascending=True)

        block_height = get_index(snapshots, df)
        # print(block_height)
        balances = get_balances(block_height, df)

        with open("balances_check.csv", "a") as fd:
            fd.write(f"{address}, " + ", ".join(str(x) for x in balances) + "\n")


if __name__ == "__main__":
    main()
