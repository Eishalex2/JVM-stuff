import pandas as pd

df = pd.read_excel('../CA MLS A-Y.xlsx')

header = df.columns.tolist()
header[0] = "List Agent First Name"

df_list = df.values.tolist()
keywords = ["cash only", "cash offer", "cash buyer", "cash sale", "cash transaction only", "hard money", "55+", "senior community", "no financing", "no loan", "commercial", "construction loan"]
keep = []
bad = []


#Number is for Confidential remarks. Assuming column C
for list in df_list:
  if type(list[2]) == float:
    keep.append(list)
  elif any(keyword in list[2].lower() for keyword in keywords):
    bad.append(list)
  else:
    keep.append(list)

#Assuming names in column Agit 
names = []
for list in keep:
  split_name = list[0].split()
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
  first_name.append(name[0].title())
  last_name.append(name[1].title())

keep_df = pd.DataFrame(keep, columns=header)
keep_df["List Agent First Name"] = first_name
keep_df.insert(1, "List Agent Last Name", last_name)

bad_df = pd.DataFrame(bad, columns=header)

with pd.ExcelWriter("CA.xlsx") as writer:
  keep_df.to_excel(writer, sheet_name="keep_ca")
  bad_df.to_excel(writer, sheet_name="filt-out_ca")