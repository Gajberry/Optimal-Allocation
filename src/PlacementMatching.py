from hospitalgenerator import hospitalgenerator
from possibilitygenerator import possibilitygenerator
from placementgenerator import placementgenerator
from placementgenerator2 import placementgenerator2
from placementsfromhosps import placementsfromhosps
from preferencesgenerator import preferencesgenerator
from copy import deepcopy
import time
import random
import csv

time1 = time.time()
hospitals=[]
placements_available={}
firstchoice=1
secondchoice=2
thirdchoice=3
try:
    with open('hospitals.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0]!='Hospital':
                if row[0] not in hospitals:
                    hospitals.append(row[0])
                if row[0] not in placements_available.keys():
                    placements_available[row[0]]=[row[1]]
                else:
                    placements_available[row[0]].append(row[1])

    people=[]
    hospital_possibilities={}
    # placements_done={}
    try:
        with open('students.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[0]!='Student Name':
                    if row[0] not in people:
                        people.append(row[0])
                    if row[0] not in hospital_possibilities.keys():
                        hospital_possibilities[row[0]]=[row[1]]
                    else:
                        if row[1] not in hospital_possibilities[row[0]]:
                            hospital_possibilities[row[0]].append(row[1])
                    # if row[0] not in placements_done.keys():
                    #     placements_done[row[0]]=[row[2]]
                    # else:
                    #     if row[1] not in placements_done[row[0]]:
                    #         placements_done[row[0]].append(row[2])
        random.shuffle(people)
        try:
            with open('preferences.csv', newline='') as csvfile:
                preferencesDict = {}
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    if row[0] != "Student Name":
                        preferencesDict[row[0]] = [row[1], row[2], row[3]]
            NurseVal = 'N'
            PlacementVal = 'P'
            HospitalVal = 'H'
            with open('Allocation.csv', 'w', newline="") as csvfile2:
                filewriter2 = csv.writer(csvfile2, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for hospital in hospitals:
                    nurses = []
                    newpeople=[]
                    for person in people:
                        if hospital_possibilities[person][0]==hospital:
                            newpeople.append(person)
                    for person in newpeople:
                        nurses.append(NurseVal + '{0}'.format(newpeople.index(person)))
                    nurse_to_people = {}
                    for nurse in nurses:
                        nurse_to_people[nurse] = newpeople[nurses.index(nurse)]
                    # print(nurse_to_people)
                    # core_placements = placementgenerator(0)
                    optional_placements = placements_available[hospital]#["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R"]
                    #["Admissions", "Bariatrics", "Burns", "Cardiac", "Dentistry", "Dermatology", "Diabetes",
                                                   # "District Nursing", "Elderly Care", "Endocrine", "Endoscopy", "ENT", "Gastro", "Gynae",
                                                   # "Haematology", "Head and Neck", "HIV", "Imaging", "Infectious Diseases","Intensive Care",
                                                   # "Liver", "Neuro", "Opthalmology", "Oncology", "Orthopaedics", "Palliative Care",
                                                   # "Plastics","Renal", "Respiratory", "Sexual Health", "Sickle Cell", "Stroke",
                                                   # "Theatres","Thoracic", "Vascular"]

                    preferences = preferencesDict
                    # Is it better for one person to get 1st  choice and another 3rd, or 2nd and 2nd?

                    # Creating the Graph
                    Vertices = []
                    for x in range(0, len(newpeople)):
                        Vertices.append(NurseVal + '{0}'.format(x))
                    for y in placements_available[hospital]:
                        x=hospitals.index(hospital)
                        Vertices.append(HospitalVal + '{0}'.format(x) + PlacementVal + str(optional_placements.index(y)))
                    # print(Vertices)
                    Edges = []
                    Weights = []
                    for nurse in newpeople:
                        # for hospital in hospitals:
                        #     if hospital in hospital_possibilities[nurse]:
                        for placement in placements_available[hospital]:
                            Edges.append([NurseVal + '{0}'.format(newpeople.index(nurse)),
                                          HospitalVal + str(hospitals.index(hospital)) + PlacementVal + str(
                                              optional_placements.index(placement))])
                            if placement in preferences[nurse]:
                                value = preferences[nurse].index(placement)
                                if value==0:
                                    weight=firstchoice
                                elif value==1:
                                    weight=secondchoice
                                elif value==2:
                                    weight=thirdchoice
                                Weights.append(weight)
                            else:
                                Weights.append(len(nurses) * (thirdchoice) + 1)
                    # print('Edges: ' + str(Edges))
                    # print('Weights: ' + str(Weights))
                    Edge_dict_for_peeps = {}
                    counter = 0
                    for nurse in newpeople:
                        edges_to_nurse = []
                        while counter < len(Edges) and Edges[counter][0] == NurseVal + '{0}'.format(newpeople.index(nurse)):
                            edges_to_nurse.append([Edges[counter][1], Weights[counter]])
                            counter += 1
                        Edge_dict_for_peeps[nurse] = edges_to_nurse
                    # print('Edge dictionary for nurses: ' + str(Edge_dict_for_peeps))

                    # Creating the First Min Weight matching
                    taken_placements = []
                    matching_edges = []
                    matching_nodes = []
                    for nurse in newpeople:
                        for edge in Edge_dict_for_peeps[nurse]:
                            if edge[1] == 1 and edge[0] not in taken_placements:
                                taken_placements.append(edge[0])
                                matching_edges.append([NurseVal + '{0}'.format(newpeople.index(nurse)), edge[0]])
                                matching_nodes.append(NurseVal + '{0}'.format(newpeople.index(nurse)))
                                matching_nodes.append(edge[0])
                                break

                    # print('Taken Placements: ' + str(taken_placements))
                    # print('Matching Edges: ' + str(matching_edges))
                    nurses_with_placements = []
                    for edge in matching_edges:
                        nurses_with_placements.append(edge[0])
                    nurses_without_placements = deepcopy(nurses)
                    for nurse in nurses_with_placements:
                        nurses_without_placements.remove(nurse)
                    # print('Nurses without placements: ' + str(nurses_without_placements))

                    while nurses_without_placements != []:
                        # print("MatchingEdges: "+str(matching_edges))
                        # print(matching_edges)
                        current_paths = []
                        current_weights = []
                        check2 = 0
                        for nurse in nurses_without_placements:
                            current_weights.append(0)
                            current_paths.append([])
                            current_paths[check2].append(nurse)
                            check2 += 1
                        finishedpaths = []
                        finishedpathsweights = []
                        while current_paths != []:
                            # print("MatchingEdges: "+str(matching_edges))
                            # print(current_paths)
                            next_paths = []
                            next_weights = []
                            for path in current_paths:
                                # print("Path: "+ str(path))
                                endnode = path[-1]
                                weight = current_weights[current_paths.index(path)]
                                if endnode[0] == HospitalVal:
                                    # print("Matching Nodes: " +str(matching_nodes))
                                    if endnode in matching_nodes:
                                        nextnode = None
                                        check = 0
                                        while nextnode is None:
                                            # print("MatchingEdges: "+str(matching_edges))
                                            # print(check)
                                            if endnode in matching_edges[check]:
                                                if len(path) > 1 and matching_edges[check][0] not in path:
                                                    nextnode = matching_edges[check][0]
                                                    new_edge_weight = Weights[Edges.index(matching_edges[check])]
                                                else:
                                                    check += 1
                                            else:
                                                check += 1
                                        path.append(nextnode)

                                        next_paths.append(path)
                                        next_weights.append(weight + new_edge_weight)
                                    else:
                                        finishedpathsweights.append(weight)
                                        finishedpaths.append(path)
                                else:
                                    next_nodes = []
                                    weights = []
                                    for edge in Edges:
                                        if endnode == edge[0] and Weights[Edges.index(edge)] < 4:
                                            if edge[1] not in path:
                                                next_nodes.append(edge[1])
                                                weights.append(Weights[Edges.index(edge)])
                                    for node in next_nodes:
                                        each_path = deepcopy(path)
                                        each_path.append(node)
                                        next_paths.append(each_path)
                                        next_weights.append(weights[next_nodes.index(node)])
                            current_paths = next_paths
                            current_weights = next_weights
                            if 0 in finishedpathsweights:
                                break
                        # print('Augmenting paths: ' + str(finishedpaths))
                        # print('Augmenting paths weights: ' + str(finishedpathsweights))
                        if finishedpaths != []:
                            foundpath = False
                            minweight = 0
                            while foundpath == False:
                                for weight in finishedpathsweights:
                                    if weight == minweight:
                                        foundpath = finishedpaths[finishedpathsweights.index(weight)]
                                        break
                                minweight += 1
                            # print('Min Weight Augmenting Path: ' + str(foundpath) + ' with weight: ' + str(minweight - 1))
                            counter = 0
                            foundpath_edges = []
                            while counter < len(foundpath) - 1:
                                foundpath_edges.append([foundpath[counter], foundpath[counter + 1]])
                                counter += 1
                            # print("FoundPath: " + str(foundpath_edges))
                            for edge in foundpath_edges:
                                if edge[0][0] != NurseVal:
                                    newedge = [edge[1], edge[0]]
                                    edge = newedge
                                if edge in matching_edges:
                                    matching_edges.remove(edge)
                                else:
                                    matching_edges.append(edge)
                            matching_nodes = []
                            for edge in matching_edges:
                                if edge[0] not in matching_nodes:
                                    matching_nodes.append(edge[0])
                                if edge[1] not in matching_nodes:
                                    matching_nodes.append(edge[1])
                            nurses_with_placements = []
                            for edge in matching_edges:
                                if edge[0][0] == NurseVal:
                                    ind = 0
                                else:
                                    ind = 1
                                nurses_with_placements.append(edge[ind])
                            nurses_without_placements = deepcopy(nurses)
                            for nurse in nurses_with_placements:
                                nurses_without_placements.remove(nurse)
                            # print('Nurses without placements: ' + str(nurses_without_placements))
                        else:
                            # print('Not doable')
                            break

                    # print("Matching:" + str(matching_edges))
                    matching_weight = 0
                    for edge in matching_edges:
                        matching_weight += Weights[Edges.index(edge)]
                    # print("Weight:" + str(matching_weight))
                    final_matching={}
                    placementgoingcodeShort={}
                    # print(matching_edges)
                    totalWeight=0
                    for nurse in nurses:
                        for edge in matching_edges:
                            if nurse in edge:
                                placementgoingcode=edge[1]
                                choice=Weights[Edges.index(edge)]
                        totalWeight+=choice
                        placementgoing=hospital+': '
                        # print(hospital_possibilities)
                        counter=1
                        while placementgoingcode[-counter].isdigit():
                            counter+=1
                        counter-=1
                        code=placementgoingcode[-counter:]
                        placementgoingcodeShort[nurse]=code
                        placementgoing+=placements_available[hospital][int(code)]
                        person=nurse_to_people[nurse]
                        final_matching[person]=[placementgoing,choice]
                    avWeight=totalWeight/len(people)
                    print(avWeight)
                    print(final_matching)
                    for nurse in nurses:
                            filewriter2.writerow([nurse_to_people[nurse], hospital, placements_available[hospital][int(placementgoingcodeShort[nurse])]])

            time2=time.time()
            timetot=time2-time1
            print(timetot)
        except:
            print("No Preferences file found (preferences.csv)")
    except:
        print("No Students file found (students.csv)")
except:
    print("No Hospital file found (hospitals.csv)")



