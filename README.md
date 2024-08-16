# Optimal Allocation with Preferences using Min Weight Max Cardinality Matching (created ~2019)

This repo provides a tool to assign individuals their allocations based on their preferences. It has previously been used to assign students to placements, but it will feasibly work in any context in which each individual must be assigned one allocation.
Each individual can provide their numbered preferences of each of the different allocations.

Because of the previous usage, the individuals are called 'students', the allocations are called 'hospitals' and the preferences are called 'preferences'.


## What is required?
For this software to be applicable, there needs to be two groups: individuals and allocations. There should be at least as many allocations as individuals but the programming will likely still work if that is not the case.

## How do I run it?
There are 3 ways to run it:
### 1) Using the .exe
In the ./dist folder, fill in the csv files for the students, hospitals and preferences. Run PlacementMatching.exe in the same folder and the allocations will be produced in the 'Allocations.csv' file.
### 2) Manually running the Python files.
In the ./src folder, run the python file GUIHospitals to create the required csv files, or edit them yourself. Then run PlacementMatching.py in the same folder and the allocations will be produced in the 'Allocations.csv' file.

## How does it work?
The code converts the setup into a minimum weight maximum cardinality matching problem. The possible assignments of a student to a placement are the edges, so we want to maximise the number of allocations we can get. 
The preferences are the weights, and so we aim to minimise the total weight of the matching to get the best allocations for students from their preferences. This gives us a bipartite graph between the students and the allocations.

To do this, we extend the augmenting path approach from finding the maximum cardinality problem (also known as Kuhn's Algorithm - see [here](https://cp-algorithms.com/graph/kuhn_maximum_bipartite_matching.html) for a good explanation). 
We do this by having both augmenting paths and improvements to the labelling, as per the Kuhn-Munkres algorithm (see [here](https://brilliant.org/wiki/hungarian-matching/)).

This guarantees that the allocation cannot be improved based on the parameters we give it.

## What's next?
Additional features include allowing for multiple allocations over time and grouping allocations based on their common themes. For example, each student needs to be allocated a placement in group A, B and C over their 6 placements.
Another feature would be to add in a 'fairness' rating to control situations which are equal in weight but less fair. For example, both students getting their 2nd choice rather than one student getting their 1st and the other student getting their 3rd choice.
