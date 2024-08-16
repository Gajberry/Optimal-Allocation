from hospitalgenerator import hospitalgenerator
from possibilitygenerator import possibilitygenerator
from placementgenerator import placementgenerator
from placementgenerator2 import placementgenerator2
from placementsfromhosps import placementsfromhosps
from preferencesgenerator import preferencesgenerator
from copy import deepcopy
import time


repeats = 10000
averages = []
maxes = []
avtimes=[]
for number_of_nurses in range(10, 40):
    time1 = time.time()
    print(number_of_nurses)
    overall_weights = []
    for z in range(0, repeats):
        NurseVal = 'N'
        PlacementVal = 'P'
        HospitalVal = 'H'
        people = []
        for x in range(number_of_nurses):
            people.append(str(x))
        # people = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
        nurses = []
        for person in people:
            nurses.append(NurseVal + '{0}'.format(people.index(person)))
        nurse_to_people = {}
        for nurse in nurses:
            nurse_to_people[nurse] = people[nurses.index(nurse)]
        core_placements = placementgenerator(0)
        #optional_placements = placementgenerator2(10)
        optional_placements = ["Admissions", "Bariatrics", "Burns", "Cardiac", "Dentistry", "Dermatology", "Diabetes",
                               "District Nursing", "Elderly Care", "Endocrine", "Endoscopy", "ENT", "Gastro", "Gynae",
                               "Haematology", "Head and Neck", "HIV", "Imaging", "Infectious Diseases","Intensive Care",
                               "Liver", "Neuro", "Opthalmology", "Oncology", "Orthopaedics", "Palliative Care",
                               "Plastics","Renal", "Respiratory", "Sexual Health", "Sickle Cell", "Stroke",
                               "Theatres","Thoracic", "Vascular"]
    #1 elderly care, 1 complex care, 1 Community, 1 Surgery, 1 Medicine group 1, Try to get one of each
        core_placements_done = {}
        optional_placements_done = {}
        # hospitals = hospitalgenerator(7)
        hospitals = ["King's"]
            # , "Guy's", "South London MH", "C & NW London MH", "C London Community", "CW,RM,RB",
            #          "Imp. College", "Lewisham & Greenwich", "SW London & St. George's MH",
            #          "St George's Uni",
            #          "UCL", "W London MH"]
        #Kings={"Adult Cystic Fibrosis":"Medicine Group 1","Annie Zunz ward":"Complex Care Group 2","Brunel Ward":"Surgery"}
        hospital_possibilities = possibilitygenerator(people, hospitals)
        placements_available = placementsfromhosps(hospitals, core_placements, optional_placements)
        poss_placements = {}
        for person in people:
            individual_poss_placements = []
            for hospital in hospital_possibilities[person]:
                for offered_placement in placements_available[hospital]:
                    if offered_placement not in individual_poss_placements:
                        individual_poss_placements.append(offered_placement)
            if individual_poss_placements == []:
                print("no placements available")
                print(hospital_possibilities)
                print(placements_available)
                getout = True
                pass
            else:
                getout = False
                poss_placements[person] = individual_poss_placements
        if getout:
            pass
        try:
            preferences = preferencesgenerator(poss_placements)
        except:
            for person in people:
                print(person)
                individual_poss_placements = []
                for hospital in hospital_possibilities[person]:
                    for offered_placement in placements_available[hospital]:
                        if offered_placement not in individual_poss_placements:
                            print(offered_placement)
            print(hospital_possibilities)
            print(placements_available)
            print(poss_placements)
            print('Oops')
            pass
        # Is it better for one person to get 1st  choice and another 3rd, or 2nd and 2nd?

        # Creating the Graph
        Vertices = []
        for x in range(0, len(people)):
            Vertices.append(NurseVal + '{0}'.format(x))
        for x in range(0, len(hospitals)):
            for y in placements_available[hospitals[x]]:
                Vertices.append(HospitalVal + '{0}'.format(x) + PlacementVal + str(optional_placements.index(y)))
        Edges = []
        Weights = []
        for nurse in people:
            for hospital in hospitals:
                if hospital in hospital_possibilities[nurse]:
                    for placement in placements_available[hospital]:
                        Edges.append([NurseVal + '{0}'.format(people.index(nurse)),
                                      HospitalVal + str(hospitals.index(hospital)) + PlacementVal + str(
                                          optional_placements.index(placement))])
                        if placement in preferences[nurse]:
                            value = preferences[nurse].index(placement)
                            Weights.append(value)
                        else:
                            Weights.append(len(nurses) * 3 + 1)
        # print('Edges: ' + str(Edges))
        # print('Weights: ' + str(Weights))
        Edge_dict_for_peeps = {}
        counter = 0
        for nurse in people:
            edges_to_nurse = []
            while counter < len(Edges) and Edges[counter][0] == NurseVal + '{0}'.format(people.index(nurse)):
                edges_to_nurse.append([Edges[counter][1], Weights[counter]])
                counter += 1
            Edge_dict_for_peeps[nurse] = edges_to_nurse
        # print('Edge dictionary for nurses: ' + str(Edge_dict_for_peeps))

        # Creating the First Min Weight matching
        taken_placements = []
        matching_edges = []
        matching_nodes = []
        for nurse in people:
            for edge in Edge_dict_for_peeps[nurse]:
                if edge[1] == 0 and edge[0] not in taken_placements:
                    taken_placements.append(edge[0])
                    matching_edges.append([NurseVal + '{0}'.format(people.index(nurse)), edge[0]])
                    matching_nodes.append(NurseVal + '{0}'.format(people.index(nurse)))
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
                next_paths = []
                next_weights = []
                for path in current_paths:
                    endnode = path[-1]
                    weight = current_weights[current_paths.index(path)]
                    if endnode[0] == HospitalVal:
                        if endnode in matching_nodes:
                            nextnode = None
                            check = 0
                            while nextnode is None:
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
                            if endnode == edge[0] and Weights[Edges.index(edge)] < 3:
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
                        matching_nodes.append(edge[0])
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
        overall_weights.append(matching_weight)
    # print(overall_weights)
    tot = 0
    max = 0
    for weight in overall_weights:
        if weight > max:
            max = weight
        tot += weight
    average = tot / len(overall_weights)
    # print(average)
    # print(max)
    averages.append(average)
    maxes.append(max)
    time2=time.time()
    timetot=time2-time1
    avtime=timetot/repeats
    avtimes.append(avtime)
print("Average times: "+str(avtimes))
print("Average weights: " +str(averages))
print("Maxium weights: " +str(maxes))



