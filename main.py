import pandas as pd
import json

pd.set_option("display.max.rows", 1000, "display.max.columns", 36)
df = pd.read_json(r"dataset/subset.json")
#print(df)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(df.head(3))
print("-------------------------- INFO --------------------------")
df.info()

print("-------------------------- SHAPE --------------------------")
print(df.shape)

print("-------------------------- FIRST 10 ROWS --------------------------")
print(df.head(10))

print("-------------------------- LAST 10 ROWS --------------------------")
print(df.tail(10))

print("-------------------------- LOOK AT COLUMN PER NAME ('headline') --------------------------")
print(df["headline"])

print("-------------------------- ACCESS DATA PER INDEX/'iloc (ROW)' --------------------------")
print(df.iloc[1])

print("-------------------------- DISPLAY STRINGS IN A COLUMN (ex. specific jobs 'sjuksköterska, undersköterska' in column 'headline') '.isin()' --------------------------")
yrken = ["sjuksköterska", "undersköterska"]
print(df[df["headline"].isin(yrken)])

print("-------------------------- DISPLAY ROWS WHERE THE COLUMN CONTAINS A SPECIFIC STRING ('sjuk') '.str.contains()' --------------------------")
print(df[df["headline"].str.contains("sjuk")])

print("-------------------------- DISPLAY SELECTED ROWS FROM A FILTERED DF ('sjuk') '.str.contains()' --------------------------")
sorterade = df[df["headline"].str.contains("sjuk")]
    # axis = 1 för att filtrera bland kolumner, 0 för rader 
print(sorterade.filter(items = ["working_hours_type", "headline"], axis = 1))


print("-------------------------- DISPLAY SELECTED ROWS FROM A FILTERED DF AND ONLY SHOWS 'last_publication_date' after 2006-12-31  ('sjuk') '.str.contains()' --------------------------")
print(sorterade[sorterade["last_publication_date"] > "2006-12-31"])
    # sort_values gör att man kan sortera för värden inom en kolumn, här med datum
    # för mer info om sortering se: https://youtu.be/kB7FV-ijdqE?si=B8kDfABae9009dXR&t=562
print(sorterade[sorterade["last_publication_date"] > "2006-12-31"].sort_values(by = "last_publication_date"))


print("-------------------------- SORT AND FOR SJUK AND SETS THE INDEX AS EMPLOYER --------------------------")
sorterade_2 = df[df["headline"].str.contains("sjuk")]
indexerat = sorterade_2.set_index("employer")
print(indexerat)






"""
with open (("dataset/subset.json"), "r") as file:
    data = json.load(file)

jobtech_dataset = pd.json_normalize(data)
print(jobtech_dataset.columns)
"""



#print(data)


