import pandas as pd

df = pd.read_excel('../Citi Home Run CA.xlsx')

header = df.columns.tolist()
#Assuming listing agent name is column A
header[0] = "List Agent First Name"

df_list = df.values.tolist()
#list of keywords to filter out into the 'bad' worksheet
keywords = ["hard cash","oyo", "own your own", "retirement community", "time share", "cash only", "cash offers only", "cash sale", "cash transaction only", "hard money", "55+", "senior community", "no financing", "no loan", "construction loan"]
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

#Number is for Confidential remarks. Assuming column I
#Filtering out the above keywords
for list in df_list:
  if type(list[8]) == float:
    keep.append(list)
  elif any(keyword in list[8].lower() for keyword in keywords):
    bad.append(list)
  else:
    keep.append(list)

#capitalize addresses, assuming column D
for list in keep:
   lower_address = list[3].lower()
   list[3] = capitalize_address(lower_address)

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

with pd.ExcelWriter("CA Actives.xlsx") as writer:
  keep_df.to_excel(writer, sheet_name="keep_ca")
  bad_df.to_excel(writer, sheet_name="filt-out_ca")