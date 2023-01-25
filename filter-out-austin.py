import pandas as pd

df = pd.read_excel('../Austin Listing Agent Stale .xlsx')

header = df.columns.tolist()
header[1] = "List Agent First Name"

df_list = df.values.tolist()
keywords = ["cash only", "cash offers", "hard money", "55+", "senior community", "no financing", "no loan", "commercial", "construction loan"]
filtered = []
bad = []

#number is the Private Remarks Column. Assuming in column D.
for list in df_list:
  if type(list[3]) == float:
    filtered.append(list)
  elif any(keyword in list[3].lower() for keyword in keywords):
    bad.append(list)
  else:
    filtered.append(list)

#Assuming full name is in column B
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