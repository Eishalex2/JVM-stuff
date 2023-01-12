import pandas as pd
import re

df = pd.read_excel('MLS Austin listings_DE-DUPED.xlsx')

header = df.columns.tolist()
header[1] = "List Agent First Name"
""" header.insert(2, "List Agent Last Name")
print(header) """

df_list = df.values.tolist()
keywords = ["cash only", "cash offers", "hard money", "55+", "senior community", "no financing", "no loan", "commercial", "construction loan"]
filtered = []
bad = []

for list in df_list:
  if type(list[22]) == float:
    filtered.append(list)
  elif any(keyword in list[22].lower() for keyword in keywords):
    bad.append(list)
  else:
    filtered.append(list)

names = []
for list in filtered:
  split_name = list[1].split()
  names.append(split_name)

for nameset in names:
  middle_last = nameset[1]
  if len(middle_last) == 1 or middle_last[1] == ".":
    nameset.pop(1)
  if len(nameset) > 2:
    nameset[1] = " ".join(nameset[1:])
    del nameset[2:]

first_name = []
last_name = []
for name in names:
  first_name.append(name[0])
  last_name.append(name[1])

filtered_df = pd.DataFrame(filtered, columns=header)
filtered_df["List Agent First Name"] = first_name
filtered_df.insert(2, "List Agent Last Name", last_name)

bad_df = pd.DataFrame(bad, columns=header)

with pd.ExcelWriter("Austin.xlsx") as writer:
  filtered_df.to_excel(writer, sheet_name="keep_austin")
  bad_df.to_excel(writer, sheet_name="filt-out_austin")