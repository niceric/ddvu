import pandas as pd
import json


with open("stopwords.txt", "r") as file:
    stopwords = file.read().replace("\n", " ")
stopwords_list = stopwords.split()


def get_number_of_words(text):
    #counter = 0 
    total_words = text.split()
    words = {}
 
    for word in total_words:
        lowered = word.lower()
        if lowered not in stopwords_list:
            if lowered in words:
                words[lowered] += 1
                #counter += 1
            else: 
                words[lowered] = 1            
            #counter += 1

    return words

def get_list_of_words(text):
        count_of_words = get_number_of_words(text)
        x = []

        
        def create_list(text):
            for item in count_of_words:
                if item.isalpha():
                    temp_dict = dict(char = item, num = count_of_words[item])
                    x.append(temp_dict)
                    
        
            def sort_on(dict):
                return dict["num"]
            x.sort(reverse=True, key=sort_on)
        
        create_list(count_of_words)
        return x




pd.set_option("display.max.rows", 1000, "display.max.columns", 36)
with open('dataset/2023.json', 'r') as file: 
    data = json.load(file)
df = pd.json_normalize(data)


#df = pd.read_json(r"dataset/subset.json")
#df = df.json_normalize(df)

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


#print("-------------------------- SORT FOR SJUK AND SETS THE INDEX AS EMPLOYER --------------------------")

#indexerat = sorterade_2.set_index("employer")
#print(indexerat)


# Skriver ut annonserna med index 0, 1, 2 utifrån den sorterade och indexerade listan ovan
sorterade_2 = df[df["headline"].str.contains("sjuk")]
print(sorterade_2.iloc[1], sorterade_2.iloc[0], sorterade_2.iloc[2])



# Räknar ut antalet värden inom en column, label, och skriver ut hur många det finns av varje
working_hours_type = df["working_hours_type.label"]
print(working_hours_type.value_counts())

# Skriver ut all data för kolumnen working_hours_type där "sjuk" omnämns i headline  
sorterade_2 = df[df["headline"].str.contains("sjuk", "vård")]
test_1 = sorterade_2["working_hours_type.label"]
print(test_1)
print(test_1.value_counts())

# gör om ovanstående till en lista och skriver endast ut "label" för denna kolumns data
list_of_working_hours = test_1.tolist()
print(list_of_working_hours)
#for listing in list_of_working_hours:
#    print()

print(len(list_of_working_hours))
#print(df)
text_labels = sorterade_2["description.text"]
list_of_labels = text_labels.tolist()
print(len(list_of_labels))

dict_of_all_words = {}
list_of_all_words = []
for label in list_of_labels:
    
    print(label)
    print(f"-- Antal ord i annonsen: ")
    get_list_of_words(label)
    for new_dict in get_list_of_words(label):
        dict_of_all_words[new_dict["char"]] = new_dict["num"]
        list_of_all_words.append(f"Ordet: '{new_dict["char"]}' fanns {new_dict["num"]} gånger.")
        print(f"Ordet: '{new_dict["char"]}' fanns {new_dict["num"]} gånger.")
    print("--------------------------------------------------- NEXT")
sort_dict_of_words = sorted(dict_of_all_words.items(), key = lambda x:x[1], reverse=True)
print(f"SUPERLISTA: {sort_dict_of_words}")


    #print(get_list_of_words(label))
    
    #for dict in get_list_of_words(label):         
    #    print(f"The '{dict["char"]}' character was found {dict["num"]} times.")
    #    print("--------------------------------------------------- NEXT")

#print(text_labels[907])
#for label in text_labels:
#    print(label)



"""
with open (("dataset/subset.json"), "r") as file:
    data = json.load(file)

jobtech_dataset = pd.json_normalize(data)
print(jobtech_dataset.columns)
"""



#print(data)


