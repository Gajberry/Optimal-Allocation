import csv
import copy
import random

hospitals = []
people = []
hospital_possibilities = {}
placements_done = {}
areas_done = {}
placements_available = {}

with open('hospitals.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[0] != 'Hospital':
            if row[0] not in hospitals:
                hospitals.append(row[0])
            if row[0] not in placements_available.keys():
                placements_available[row[0]] = [row[1]]
            else:
                placements_available[row[0]].append(row[1])

with open('students.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        rowlength=len(row)
        if row[0] != 'Student Name':
            if row[0] not in people:
                people.append(row[0])
            if row[0] not in hospital_possibilities.keys():
                hospital_possibilities[row[0]] = [row[1]]
            else:
                if row[1] not in hospital_possibilities[row[0]]:
                    hospital_possibilities[row[0]].append(row[1])
            placements_done[row[0]] = []
            checker=2
            while checker<rowlength:
                if row[checker]!='':
                    placements_done[row[0]].append(row[checker])
                checker+=1
print(placements_done)

poss_placements = {}
for person in people:
    individual_poss_placements = []
    for hospital in hospital_possibilities[person]:
        for offered_placement in placements_available[hospital]:
            individual_poss_placements.append(offered_placement)
        if individual_poss_placements == []:
            print("No placements available for " + str(person))
            poss_placements[person]=hospital_possibilities[person]
        else:
            poss_placements[person] = individual_poss_placements

Groups = [['A', 'B'], ['C', 'D'],['E']] #This needs to include ALL placements
Required_groups = [1]
Groups_counter={}
for person in people:
    counter_array=[]
    for group in Groups:
        counter=0
        for placement in placements_done[person]:
            if placement in group:
                counter+=1
        counter_array.append(counter)
    Groups_counter[person]=counter_array
Overall_options={}
for person in people:
    Overall_options[person]=[]
    counter=0
    while counter not in Groups_counter[person]:
        counter+=1
    poss_groups=[]
    for x in range(0,len(Groups)):
        if Groups_counter[person][x]==counter:
            poss_groups.append(x)
    required_poss=[]
    for poss in poss_groups:
        if poss in Required_groups:
            required_poss.append(poss)
    if required_poss!=[]:
        group_choosing=required_poss
    else:
        group_choosing = poss_groups
    for next_group in group_choosing:
        for placement in Groups[next_group]:
            if placement in poss_placements[person]:
                Overall_options[person].append(placement)


print(Overall_options)
with open('options.csv', 'w',newline='') as csvfile:
    filewriter=csv.writer(csvfile, delimiter=',',
               quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["Student Name","Options"])
    for person in people:
        entry=[person]
        for option in Overall_options[person]:
            entry.append(option)
        filewriter.writerow(entry)
#
# Groups_done = {}
# for person in people:
#     Groups_done[person] = []
#     for group in Groups:
#         for placement in group:
#             if placement in placements_done[person]:
#                 Groups_done[person].append(Groups.index(group))
#                 break
# print(Groups_done)
# for person in people:
#     for groupnum in Groups_done[person]:
#         for placement in Groups[groupnum]:
#             if placement in poss_placements[person]:
#                 poss_placements[person].remove(placement)
# Groups_to_do = {}
# Required_groups = [1]
# for person in people:
#     Groups_to_do[person] = copy.deepcopy(Required_groups)
#     for groupnum in Groups_done[person]:
#         if groupnum in Groups_to_do[person]:
#             Groups_to_do[person].remove(groupnum)
#     if Groups_to_do[person] == []:
#         print(str(person) + "- All done!")
#         counters={}
#         for group in Groups:
#             counters[str(Groups.index(group))]=0
#
#         Groups_to_do[person]="Finished"
# print(Groups_to_do)
# for person in people:
#     poss_placements_to_do = []
#     if Groups_to_do[person] != []:
#         groupnum = random.choice(Groups_to_do[person])
#         print(groupnum)
#         newplacements = []
#         for placement in poss_placements[person]:
#             if placement in Groups[groupnum]:
#                 newplacements.append(placement)
#         poss_placements[person] = newplacements
#         #     poss_placements_to_do.append(placement)
#         #     # for groupnum in Groups_to_do[person]:
#         # for placement in Groups[groupnum]:
#         #     poss_placements_to_do.append(placement)
#         # for placement in poss_placements[person]:
#         #     if placement not in poss_placements_to_do:
#         #         poss_placements[person].remove(placement)
#
# print(poss_placements)
