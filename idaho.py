import pandas as pd

df = pd.read_excel('../Austin.xlsx')

header = df.columns.tolist()
header[0] = "List Agent First Name"

df_list = df.values.tolist()
keywords = ["retirement community", "time share", "cash only", "cash offers", "hard money", "55+", "senior community", "no financing", "no loan", "construction loan"]
keep = []
bad = []

#number is the Private Remarks Column. Assuming in column E.
for list in df_list:
  #Make the addresses title case. Assuming Column C
  list[2] = list[2].lower().title()
  if type(list[4]) == float:
    keep.append(list)
  elif any(keyword in list[4].lower() for keyword in keywords):
    bad.append(list)
  else:
    keep.append(list)

#Assuming full name is in column A
names = []
for list in keep:
  split_name = list[0].split()
  names.append(split_name)

for nameset in names:
  if len(nameset) > 1:
    middle_last = nameset[1]
    if len(middle_last) == 1 or middle_last[1] == ".":
      nameset.pop(1)
    if len(nameset) > 2:
      nameset[1] = " ".join(nameset[1:])
      del nameset[2:]

first_name = []
last_name = []
for name in names:
  first_name.append(name[0].lower().title())
  if len(name) > 1:
    last_name.append(name[1].lower().title())
  else:
    last_name.append('')

filtered_df = pd.DataFrame(keep, columns=header)
filtered_df["List Agent First Name"] = first_name
filtered_df.insert(1, "List Agent Last Name", last_name)

bad_df = pd.DataFrame(bad, columns=header)

with pd.ExcelWriter("Idaho.xlsx") as writer:
  filtered_df.to_excel(writer, sheet_name="keep_idaho")
  bad_df.to_excel(writer, sheet_name="filt-out_idaho")