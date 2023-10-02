import pandas as pd

df = pd.read_excel('../ADU Contractors.xlsx')

header = df.columns.tolist()
df_list = df.values.tolist()

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

#Capitalize addresses. Indexing starts at 0
for list in df_list:
  lower_address = list[4].lower()
  list[4] = capitalize_address(lower_address)

general_df = pd.DataFrame(df_list, columns=header)

general_df.to_excel("../ADU Contractors formatted addresses.xlsx")