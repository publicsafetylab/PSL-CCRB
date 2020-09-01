import json

import pandas as pd

columns_map = json.load(open("census-col-lookup.json", "r"))
df = pd.read_csv("raw/census_precinct.csv", index_col=0)
df = df.rename(columns=columns_map)
df = df.drop([x for x in df.columns if x.startswith("P00")], axis=1)
records = df.to_dict(orient="records")


black_columns = [c for c in df.columns if c.startswith("R_") and "B" in c]
nh_black_columns = [c for c in df.columns if c.startswith("NH_") and "B" in c]
nh_asian_columns = [c for c in df.columns if c.startswith("NH_") and "A" in c and "B" not in c]

for r in records:
    r["Black"] = sum([r[c] for c in black_columns])
    r["NH_Black"] = sum([r[c] for c in nh_black_columns])  # intermediate
    r["H_Black"] = r["Black"] - r["NH_Black"]  # intermediate
    r["Hispanics"] = r["Hispanics"] - r["H_Black"]
    r["NH_Asian"] = sum([r[c] for c in nh_asian_columns])
    r["NH_White"] = r["NH_W"]
    r["Others"] = r["Total_Population"] - r["Black"] - r["Hispanics"] - r["NH_Asian"] - r["NH_White"]

new_df = pd.DataFrame.from_dict(records)
new_df = new_df.dropna(subset=["precinct_2020"])
precincts_group = new_df.groupby("precinct_2020")
precincts_demo = precincts_group[["Total_Population", "Black", "Hispanics", "NH_Asian", "NH_White", "Others"]].sum().reset_index()
precincts_demo.to_csv("precincts_demos.csv")



