import pandas as pd

df = pd.read_excel('MLS-Austin-listings.xlsx')

header = df.columns.tolist()

df_list = df.values.tolist()
keywords = ["cash only", "hard money only", "55+", "senior community", "no financing", "no loan", "commercial", "construction loan"]
filtered = []
bad = []

for list in df_list:
  if type(list[22]) == float:
    filtered.append(list)
  elif any(keyword in list[22].lower() for keyword in keywords):
    bad.append(list)
  else:
    filtered.append(list)

filtered_df = pd.DataFrame(filtered, columns=header)
bad_df = pd.DataFrame(bad, columns=header)

with pd.ExcelWriter("Austin.xlsx") as writer:
  filtered_df.to_excel(writer, sheet_name="keep_austin")
  bad_df.to_excel(writer, sheet_name="filt-out_austin")