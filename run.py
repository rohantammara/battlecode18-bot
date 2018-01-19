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
tryRotate = [0,-1,1,-2,2]
mining =  True
corpus = []

print("TestStarter")

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)
prev_dir = bc.Direction.Center

my_team = gc.team()
print(my_team)

def Karbonite_Mining(id,directions,prev_dir):
    karbonite_collected = False
    for d in directions:
        if gc.can_harvest(id, d):
            gc.harvest(id, d)
            prev_dir = d
            karbonite_collected = False
            break
        else:
            karbonite_collected = True

    if  karbonite_collected == True and gc.is_move_ready(id) and gc.can_move(id, prev_dir):
        gc.move_robot(id, prev_dir)
    return (prev_dir)

def rotate(dir,amount):
    ind = directions.index(dir)
    return directions[(ind+amount)]

def fuzzygoto(unit,dest):
    toward = unit.location.map_location().direction_to(dest)
    for tilt in  tryRotate:
        d = rotate(toward,tilt)
        if gc.can_move(unit.id,d):
            gc.move_robot(unit.id,d)
            break
earthMap =  gc.starting_map(bc.Planet.Earth)

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
                    prev_dir = Karbonite_Mining(unit.id,directions,prev_dir)
                    for loc in gc.all_locations_within(location.map_location(),9):
                        if gc.karbonite_at(loc) != 0:
                            mining = True
                            break
                        else:
                            mining = False
                    if mining == False:
                        corpus.remove(unit.id)
                        if len(corpus) == 0:
                            mining = False
                        else:
                            mining = True
## Path-Finding
            if mining == False:
                dest = bc.MapLocation(bc.Planet.Earth,(earthMap.width),(earthMap.height))
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
