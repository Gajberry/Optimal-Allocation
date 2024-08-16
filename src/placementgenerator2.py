def placementgenerator2(num):
    placements=[]
    for x in range(0,num):
        placements.append('OptPlacement{0}'.format(x))
    return placements