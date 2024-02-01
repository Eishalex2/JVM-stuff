import pandas as pd

df = pd.read_excel('../Dallas List (1).xlsx')

header = df.columns.tolist()
header[0] = "List Agent First Name"

df_list = df.values.tolist()
keywords = ["hard cash", "ccrc", "own your own", "retirement community", "time share", "timeshare", "cash only", "cash offers only", "cash buyer", 
            "cash sale", "cash transaction only", "hard money", "hard money only", "55+", "senior community", "no financing", "no loan", "construction loan", 
            "private money", "leased-land", "leased land", "land lease"]
keep = []
bad = []

def capitalize_address(address):
    words = address.split(' ')
    capitalized_words = []

    # Loop through each word in the address
    for i, word in enumerate(words):
        # Capitalize the word if it meets the specified conditions
        if i == 0 or (len(word) > 2 and word[:2].upper() == word[:2]):
            capitalized_words.append(word.capitalize())
        elif i == 1 and len(word) == 2 and word.isalpha() and word.islower():
            capitalized_words.append(word.upper())
        else:
            capitalized_words.append(word.capitalize())

    # Join the words back into a single string
    capitalized_address = ' '.join(capitalized_words)
    return capitalized_address


for list in df_list:
  if list[5] == "Cash":
    bad.append(list)
  else: 
    keep.append(list)

#number is the Private Remarks Column. Assuming in column E.
for list in keep:
  if type(list[7]) == float:
    continue
  elif any(keyword in list[7].lower() for keyword in keywords):
    bad.append(list)
    keep.remove(list)

for list in keep:
    #Make the addresses title case. Assuming Column C
    lower_address = list[2].lower()
    list[2] = capitalize_address(lower_address)


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

with pd.ExcelWriter("../Dallas 10.02 processed.xlsx") as writer:
  filtered_df.to_excel(writer, sheet_name="keep_dallas")
  bad_df.to_excel(writer, sheet_name="filt-out_dallas")