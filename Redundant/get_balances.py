import numpy as np
import pandas as pd

    def get_balances(block_heights: list[int], dataframe: pd.DataFrame) -> list:
    """Check the transaction before the index to see what the balance was"""
    balances = []
    num_rows = dataframe.shape[0]
    for index, block in enumerate(block_heights):
        if block == num_rows - 1:
            balances.append(0)
            dataframe.drop(dataframe.index[dataframe["Block"] == block], inplace=True)
            continue
        try:
            value = dataframe["Total"].loc[(block + 1)]
            if block <= len(block_heights):
                balances += [value] * (len(block_heights) - index)
                dataframe.drop(
                    dataframe.index[dataframe["Block"] == block], inplace=True
                )
                break
            # Check if rest of snapshots were missed
            balances.append(value)
        except KeyError:
            print(f"Error at {block}")
            balances.append("Error")

    # Fix all values not affected by transactions
    for index, block in enumerate(balances):
        try:
            if balances[index + 1] == "Test_Block":
                balances[index + 1] = block
        except IndexError:
            continue
    return balances
