import random
import copy

def placementsfromhosps(hospitals,coreplacements,optionalplacements):
    combined=[coreplacements,optionalplacements]
    placementdict={}
    for hospital in hospitals:
        newcombined=copy.deepcopy(combined)
        totalplacements=random.randint(15,15)
        offeredplacements=[]
        for x in range(0,totalplacements):
            if len(newcombined[0])==0:
                coreopt=1
            elif len(newcombined[1])==0:
                coreopt=0
            else:
                coreopt=random.randint(0,1)
            chosenplacement=random.randint(0,len(newcombined[coreopt])-1)
            offeredplacements.append(newcombined[coreopt][chosenplacement])
            newcombined[coreopt].remove(newcombined[coreopt][chosenplacement])
        placementdict[hospital]=offeredplacements
    return placementdict