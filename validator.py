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

    pd.DataFrame([[block, 0, 0]], columns=["Block", "Data/Time", "Total"])
    dataframe.loc[len(dataframe.index)] = [block, 0, 0]
    return dataframe


def get_index(blocks: list[str], dataframe: pd.DataFrame) -> list[int]:
    """Get the index of the dummy blocks that were inserted"""
    indices = []
    for block in blocks:
        indices.append(np.flatnonzero(dataframe["Block"] == int(block))[0])
    return indices


def get_balances(order: list[int], dataframe: pd.DataFrame) -> list:
    """Check the transaction before the index to see what the balance was"""
    balances = []
    num_rows = dataframe.shape[0]
    for index, block in enumerate(order):
        if block == num_rows - 1:
            balances.append(0)
            continue
        try:
            value = dataframe["Total"].loc[(block + 1)]
            if block < len(order):
                balances += [value] * (len(order) - index)
                break
            # Check if rest of snapshots were missed
            balances.append(value)
        except KeyError:
            balances.append("NaN")
            print(f"Error at {block}")
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
        df = df.sort_values("Block", axis=0, ignore_index=True, ascending=False)
        indices = get_index(snapshots, df)

        balances = get_balances(indices, df)

        with open("balances_check.csv", "a") as fd:
            fd.write(f"{address}, " + ", ".join(str(x) for x in balances) + "\n")


if __name__ == "__main__":
    main()
