import random
import copy

def possibilitygenerator(people,hospitals):
    hospitalpossibilities={}
    for person in people:
        choices=[]
        hospitalspecific = copy.deepcopy(hospitals)
        for x in range(0,1):
            hosp=random.choice(hospitalspecific)
            hospitalspecific.remove(hosp)
            choices.append(hosp)
        hospitalpossibilities[person]=choices
    return hospitalpossibilities
