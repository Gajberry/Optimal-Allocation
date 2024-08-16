import random
from copy import deepcopy

def preferencesgenerator(poss_placements):
    preferences={}
    temp_poss_placements=deepcopy(poss_placements)
    for person in temp_poss_placements.keys():
        if temp_poss_placements[person]==[]:
            print(poss_placements)
        firstchoice=random.choice(temp_poss_placements[person])
        temp_poss_placements[person].remove(firstchoice)
        secondchoice = random.choice(temp_poss_placements[person])
        temp_poss_placements[person].remove(secondchoice)
        try:
            thirdchoice = random.choice(temp_poss_placements[person])
        except:
            thirdchoice=None
        preferences[person]=[firstchoice,secondchoice,thirdchoice]
    return preferences