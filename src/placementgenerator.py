def placementgenerator(num):
    placements=[]
    for x in range(0,num):
        placements.append('CorePlacement{0}'.format(x))
    return placements