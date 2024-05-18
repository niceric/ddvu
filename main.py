import pandas as pd
from operator import itemgetter
import re

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


df = pd.read_csv("dataset/subset_with_keywords2023.csv")


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
print(subset)


subset_description = subset["description.text"]
list_of_labels = subset_description.tolist()
print(len(list_of_labels))



def sorting_dict(dict):
    unsorted_list_of_tuples = sorted(dict.items())
    return sorted(unsorted_list_of_tuples, key=itemgetter(1))

def splitting_and_counting(list_of_text):
    giant_list = []
    for list in list_of_text:

        splitted_text = list.split()
        giant_list += splitted_text
    return giant_list

def dict_string_and_num(list):
    giant_dict = dict()
    for word in list:
        lowered_word = word.lower()
        if lowered_word not in stopwords_list and lowered_word.isalpha():
            giant_dict[lowered_word] = giant_dict.get(lowered_word, 0) + 1
    return sorting_dict(giant_dict)


total_number = dict_string_and_num(splitting_and_counting(list_of_labels)) 


print(total_number)
print(len(total_number))


pattern_for_word = re.compile(r"(\b\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s)?augmented reality(\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\s\S+\b)?")
