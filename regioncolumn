import pandas as pd

# Läs in CSV-filen och skapa subset
df = pd.read_csv('subset_with_keywords2021.csv', usecols=['application_deadline', 'headline', 'number_of_vacancies', 'publication_date', 'description.text', 'duration.label', 'employer.name', 'working_hours_type.label', 'workplace_address.municipality_code'])

# Regionslista
regions = {
    "Stockholms län": ["114", "115", "117", "120", "123", "125", "126", "127", "128", "136", "138", "139", "140", "160", "162", "163", "180", "181", "182", "183", "184", "186", "187", "188", "191", "192"],
    "Uppsala län": ["305", "319", "330", "331", "360", "380", "381", "382"],
    "Södermanlands län": ["428", "461", "480", "481", "482", "483", "484", "486", "488"],
    "Östergötlands län": ["509", "512", "513", "560", "561", "562", "563", "580", "581", "582", "583", "584", "586"],
    "Jönköpings län": ["604", "617", "642", "643", "662", "665", "680", "682", "683", "684", "685", "686", "687"],
    "Kronobergs län": ["760", "761", "763", "764", "765", "767", "780", "781"],
    "Kalmar län": ["821", "834", "840", "860", "861", "862", "880", "881", "882", "883", "884", "885"],
    "Gotlands län": ["980"],
    "Blekinge län": ["1060", "1080", "1081", "1082", "1083"],
    "Skåne län": ["1214", "1230", "1231", "1233", "1256", "1257", "1260", "1261", "1262", "1263", "1264", "1265", "1266", "1267", "1270", "1272", "1273", "1275", "1276", "1277", "1278", "1280", "1281", "1282", "1283", "1284", "1285", "1286", "1287", "1290", "1291", "1292", "1293"],
    "Hallands län": ["1315", "1380", "1381", "1382", "1383", "1384"],
    "Västra Götalands län": ["1401", "1402", "1407", "1415", "1419", "1421", "1427", "1430", "1435", "1438", "1439", "1440", "1441", "1442", "1443", "1444", "1445", "1446", "1447", "1452", "1460", "1461", "1462", "1463", "1465", "1466", "1470", "1471", "1472", "1473", "1480", "1481", "1482", "1484", "1485", "1486", "1487", "1488", "1489", "1490", "1491", "1492", "1493", "1494", "1495", "1496", "1497", "1498", "1499"],
    "Värmlands län": ["1715", "1730", "1737", "1760", "1761", "1762", "1763", "1764", "1765", "1766", "1780", "1781", "1782", "1783", "1784", "1785"],
    "Örebro län": ["1814", "1860", "1861", "1862", "1863", "1864", "1880", "1881", "1882", "1883", "1884", "1885"],
    "Västmanlands län": ["1904", "1907", "1960", "1961", "1962", "1980", "1981", "1982", "1983", "1984"],
    "Dalarnas län": ["2021", "2023", "2026", "2029", "2031", "2034", "2039", "2061", "2062", "2080", "2081", "2082", "2083", "2084", "2085"],
    "Gävleborgs län": ["2101", "2104", "2121", "2132", "2161", "2180", "2181", "2182", "2183", "2184"],
    "Västernorrlands län": ["2260", "2262", "2280", "2281", "2282", "2283", "2284"],
    "Jämtlands län": ["2303", "2305", "2309", "2313", "2321", "2326", "2361", "2380"],
    "Västerbottens län": ["2401", "2403", "2404", "2409", "2417", "2418", "2421", "2422", "2425", "2460", "2462", "2463", "2480", "2481", "2482"],
    "Norrbottens län": ["2505", "2506", "2510", "2513", "2514", "2518", "2521", "2523", "2560", "2580", "2581", "2582", "2583", "2584"]
}

# Funktion för att hämta regionen från kommunkoden
def get_region(municipality_code, regions):
    # Konvertera till sträng och ta bort decimalen och eventuell ".0"
    if pd.isnull(municipality_code):
        return "Okänd region"
    else:
        municipality_code = str(int(municipality_code))
        for region, codes in regions.items():
            if municipality_code in codes:
                return region
        return "Okänd region"  # Om kommunen inte finns i listan över regioner

# Skapa en ny kolumn 'Region' baserat på kommunkoden i ditt dataset
df['Region'] = df['workplace_address.municipality_code'].apply(lambda x: get_region(x, regions))

# Visa de första raderna av datasetet med den nya 'Region' kolumnen
print("Första raderna av datasetet med Region:")
print(df.head())

