import pandas as pd

df = pd.read_excel('../CA 4.18.xlsx')

header = df.columns.tolist()
header[0] = "List Agent First Name"

df_list = df.values.tolist()
#list of keywords to filter out into the 'bad' worksheet
keywords = ["retirement community", "time share", "cash only", "cash offer", "cash buyer", "cash sale", "cash transaction only", "hard money", "55+", "senior community", "no financing", "no loan", "construction loan"]
keep = []
bad = []


#Number is for Confidential remarks. Assuming column E
#Filtering out the above keywords
for list in df_list:
  #Make the addresses title case. Assuming column C
  list[2] = list[2].lower().title()
  if type(list[4]) == float:
    keep.append(list)
  elif any(keyword in list[4].lower() for keyword in keywords):
    bad.append(list)
  else:
    keep.append(list)

#Assuming names in column A
#Splitting listing agent names 
names = []
for list in keep:
  split_name = list[0].split()
  names.append(split_name)

#Removing middle initials and joining all full middle and last names
#into one column
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

keep_df = pd.DataFrame(keep, columns=header)
keep_df["List Agent First Name"] = first_name
keep_df.insert(1, "List Agent Last Name", last_name)

bad_df = pd.DataFrame(bad, columns=header)

with pd.ExcelWriter("CA.xlsx") as writer:
  keep_df.to_excel(writer, sheet_name="keep_ca")
  bad_df.to_excel(writer, sheet_name="filt-out_ca")