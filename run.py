import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

print("Test starting")

gc = bc.GameController()
directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East,
              bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest,
              bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,-7,-2,-6,-3,-5]
mining =  True
corpus = []
blocked =  {}

print("TestStarter")

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)


my_team = gc.team()
print(my_team)

def Karbonite_Mining(id,directions,unit,mining):
    karbonite_collected = False
    for d in list(bc.Direction):
        if gc.can_harvest(id, d):
            gc.harvest(id, d)
            karbonite_collected = False
            break
        else:
            karbonite_collected = True

    if  karbonite_collected == True and gc.is_move_ready(id):
        for i  in [1,2,3,4]:
            for loc in gc.all_locations_within(location.map_location(),5*i):
                if gc.karbonite_at(loc) != 0:
                    mining = True
                    fuzzygoto(unit,loc)
                    break
                else:
                    mining = False
            if mining ==True:
                break
    return (mining)

def rotate(dir,amount):
    ind = directions.index(dir)
    return directions[(ind+amount)]

def fuzzygoto(unit,dest):
    toward = unit.location.map_location().direction_to(dest)
    for tilt in  tryRotate:
        d = rotate(toward,tilt)
        if unit.id not in blocked.keys():
             if d == bc.Direction.North:
                 blocked[unit.id] = [bc.Direction.South,bc.Direction.Southeast,bc.Direction.Southwest]
             elif d == bc.Direction.Northeast:
                 blocked[unit.id] = [bc.Direction.Southwest,bc.Direction.South,bc.Direction.West]
             elif d == bc.Direction.East:
                 blocked[unit.id] = [bc.Direction.West,bc.Direction.Southwest,bc.Direction.Northwest]
             elif d == bc.Direction.Southeast:
                 blocked[unit.id] = [bc.Direction.Northwest,bc.Direction.North,bc.Direction.West]
             elif d == bc.Direction.South:
                 blocked[unit.id] = [bc.Direction.North,bc.Direction.Northeast,bc.Direction.Northwest]
             elif d == bc.Direction.Southwest:
                 blocked[unit.id] = [bc.Direction.Northeast,bc.Direction.North,bc.Direction.East]
             elif d == bc.Direction.West:
                 blocked[unit.id] = [bc.Direction.East,bc.Direction.Northeast,bc.Direction.Southeast]
             elif d == bc.Direction.Northwest:
                 blocked[unit.id] = [bc.Direction.Southeast,bc.Direction.South,bc.Direction.East]

        else:
            for values in blocked[unit.id]:
                if values == d:
                    stinky = True
                    break
                else:
                    stinky = False
            if stinky == False:
                if gc.can_move(unit.id,d):
                    gc.move_robot(unit.id,d)
                    break
        print(blocked[unit.id])
        print("d: ", d)

    if d == bc.Direction.North:
        blocked[unit.id] = [bc.Direction.South,bc.Direction.Southeast,bc.Direction.Southwest]
    elif d == bc.Direction.Northeast:
        blocked[unit.id] = [bc.Direction.Southwest,bc.Direction.South,bc.Direction.West]
    elif d == bc.Direction.East:
        blocked[unit.id] = [bc.Direction.West,bc.Direction.Southwest,bc.Direction.Northwest]
    elif d == bc.Direction.Southeast:
        blocked[unit.id] = [bc.Direction.Northwest,bc.Direction.North,bc.Direction.West]
    elif d == bc.Direction.South:
        blocked[unit.id] = [bc.Direction.North,bc.Direction.Northeast,bc.Direction.Northwest]
    elif d == bc.Direction.Southwest:
        blocked[unit.id] = [bc.Direction.Northeast,bc.Direction.North,bc.Direction.East]
    elif d == bc.Direction.West:
        blocked[unit.id] = [bc.Direction.East,bc.Direction.Northeast,bc.Direction.Southeast]
    elif d == bc.Direction.Northwest:
        blocked[unit.id] = [bc.Direction.Southeast,bc.Direction.South,bc.Direction.East]

earthMap =  gc.starting_map(bc.Planet.Earth)
dest = bc.MapLocation(bc.Planet.Earth,(earthMap.width) - 3,(earthMap.height)-3)

while True:
    print('pyround:', gc.round())

    try:

        for unit in gc.my_units():
            location = unit.location
## Mining
            if unit.unit_type == bc.UnitType.Worker :
                if not unit.id in corpus:
                    corpus.append(unit.id)
                if(mining==True):
                    mining = Karbonite_Mining(unit.id,directions,unit,mining)

                    if mining == False:
                        corpus.remove(unit.id)
                        if len(corpus) == 0:
                            mining = False
                        else:
                            mining = True
## This if condition only works if worker has done nothing this round.. Put suitable code here!!
            if mining ==False:
                if(unit.location.map_location().direction_to(dest)!=bc.Direction.Center):
                    blocked.clear()
                    fuzzygoto(unit,dest)

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
