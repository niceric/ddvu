import pandas as pd
import json

# Läs in JSON-filen, lägg in rätt år
with open('2021.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Använd json_normalize för att "flattena" JSON-strukturen
df = pd.json_normalize(data)

# Skriv till CSV, glöm inte ange rätt år
df.to_csv('2021.csv', index=False)

print("JSON-filen har konverterats till CSV och 'flattenats' till en DataFrame.")
