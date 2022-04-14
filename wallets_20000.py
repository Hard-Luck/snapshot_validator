import pandas as pd

df = pd.read_csv("Phore Snapshots - Graphene Airdrops - Snapshots - All.csv")
print(df)
filtered = df[
    (df["Snapshot 1"] >= 20000)
    | (df["Snapshot 2"] >= 20000)
    | (df["Snapshot 3"] >= 20000)
    | (df["Snapshot 4"] >= 20000)
    | (df["Snapshot 5"] >= 20000)
    | (df["Snapshot 6"] >= 20000)
]
ADDRESSES = filtered["PHR Address"]

if __name__ == "__main__":
    print(ADDRESSES)
