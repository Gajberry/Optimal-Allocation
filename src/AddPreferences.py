import csv

def preferencesRetrieval():
    try:
        with open('preferences.csv', newline='') as csvfile:
            preferencesDict={}
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[0]!="Student Name":
                    preferencesDict[row[0]]=[row[1],row[2],row[3]]
        return preferencesDict
    except:
        print("No Preferences file found (preferences.csv)")
        return None