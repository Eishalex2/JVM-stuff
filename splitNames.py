import pandas as pd

df = pd.read_excel('../TX Retirement.xlsx')

header = df.columns.tolist()
header[0] = "First Name"
df_list = df.values.tolist()

names = []
for list in df_list:
  split_name = list[0].split()
  names.append(split_name)

for nameset in names:
  if len(nameset) > 1:
    middle_or_last = nameset[1]
    if len(middle_or_last) == 1 or middle_or_last[1] == ".":
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
  #handle the edge case where there's no 2nd name
  else:
    last_name.append('')

lawyers_df = pd.DataFrame(df_list, columns = header)
lawyers_df["First Name"] = first_name
lawyers_df.insert(1, "Last Name", last_name)

lawyers_df.to_excel("../Retirement TX split names.xlsx")