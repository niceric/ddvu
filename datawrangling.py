import pandas as pd
import json
from urllib.request import urlretrieve
from zipfile import ZipFile


print("..-- Data wrangling of data sets from jobtech --..")
print("Please select which year you would like to run the data cleaning and filtering on: ")
print("2006, 2007, 2008, 2009, 20010 ...")
selected_year = input("Write the year: ")

# Downloads from:
# https://data.jobtechdev.se/annonser/historiska/index.html
url = f"https://data.jobtechdev.se/annonser/historiska/{selected_year}.zip"


print(f"Starting the process on the year {selected_year}... Downloading the file...")
path, header = urlretrieve(url, filename=f"dataset/{selected_year}.zip")
print("Downloaded the file... Starting unziping...")

with ZipFile(f"dataset/{selected_year}.zip", "r") as zObject:
    zObject.extractall(path="dataset/")
print("Unziped the file... Starting the opening...")

with open(f"dataset/{selected_year}.json", "r", encoding="utf-8") as file:
    data = json.load(file)
print("Opened the file... Normalizing the data...")
df = pd.json_normalize(data)
print("Normalized the data... Converting to .csv...")
df.to_csv(f"dataset/{selected_year}.csv", index=False)

print("Converted to csv... Starting the data cleaning and filtering...: ")
#print(df.head())

# Lista med gemensamma nyckelord för vården
gemensamma_keywords = [
    "Sjuksköterska",
    "Specialistsjuksköterska",
    "Legitimerad sjuksköterska",
    "Undersköterska",
    "Vårdassistent",
    "Vårdbiträde",
    "Barnmorska",
    "Vårdpersonal",
    "Omvårdnad",
    "Sjukvård",
    "Akutsjukvård",
    "Primärvård",
    "Intensivvård",
    "Omvårdnadspersonal",
    "Vårdområdet",
    "Omsorgsarbetare",
    "Vårdsamordnare",
    "Äldreomsorg",
    "Hemtjänst",
    "Gynekologi",
    "Gynekologisk vård",
    "Graviditetsvård",
    "Förlossning",
    "Mödra- och barnhälsovård",
    "Förlossningsavdelning"
]

# Skapa ett filter baserat på nyckelorden för vården
filter_varden = df['headline'].str.contains('|'.join(gemensamma_keywords), case=False, na=False)

# Skapa subset med historiska jobbannonser som innehåller minst ett nyckelord i description.text
subset = df[filter_varden]

# Välj ut angivna kolumner
subset = subset[['application_deadline', 'headline', 'number_of_vacancies', 'publication_date', 
                 'description.text', 'duration.label', 'employer.name', 
                 'working_hours_type.label', 'workplace_address.municipality_code']]

# Konvertera kolumnen "number_of_vacancies" till numerisk form
subset['number_of_vacancies'] = pd.to_numeric(subset['number_of_vacancies'], errors='coerce')

# Printa de första 5 raderna
print(subset.head())

# Ta bort rader där antalet lediga platser är mer än 50
subset = subset[subset['number_of_vacancies'] <= 50]

# Ta bort alla exakta dubbletter i hela subsetet
subset.drop_duplicates(inplace=True)

# Ta bort rader där beskrivningstexten är saknad
subset = subset.dropna(subset=['description.text'])

# Spara subsetet som en CSV-fil
subset.to_csv(f'dataset/subset_with_keywords{selected_year}.csv', index=False)

print(f"A filterted subset has been saved with the filename: subset_with_keywords{selected_year}.csv")

