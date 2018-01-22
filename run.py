import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

print("Test starting")

gc = bc.GameController()
# Initializing code
directions = [bc.Direction.Center, bc.Direction.North, bc.Direction.Northeast,
            bc.Direction.East, bc.Direction.Southeast, bc.Direction.South,
            bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,1,-2,2]
mining = True
corpus = []
prev_dir = directions[0]
earthMap = gc.starting_map(bc.Planet.Earth)

print("TestStarter")

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(my_team)

def Karbonite_Mining(id,directions,prev_dir,unit):
    karbonite_collected = False
    for d in directions:
        if gc.can_harvest(id, d):
            gc.harvest(id, d)
            prev_dir = d
            karbonite_collected = False
            break
        else:
            karbonite_collected = True

    if  karbonite_collected == True and gc.is_move_ready(id):
        for loc in gc.all_locations_within(location.map_location(),5):
            if gc.karbonite_at(loc) != 0:
                mining = True
                fuzzygoto(unit,loc)
                break
            else:
                mining = False

        for loc in gc.all_locations_within(location.map_location(),10):
            if gc.karbonite_at(loc) != 0:
                mining = True
                fuzzygoto(unit,loc)
                break
            else:
                mining = False
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

while True:
    print('pyround:', gc.round())

    try:

        for unit in gc.my_units():
            location = unit.location
            # Mining
            if unit.unit_type == bc.UnitType.Worker:
                if unit.id not in corpus:
                    corpus.append(unit.id)
                if mining is True:
                    prev_dir = Karbonite_Mining(unit.id, directions, prev_dir, unit)
                    for loc in gc.all_locations_within(location.map_location(), 9):
                        if gc.karbonite_at(loc) != 0:
                            mining = True
                            break
                        else:
                            mining = False
                    if mining is False:
                        corpus.remove(unit.id)
                        if len(corpus) == 0:
                            mining = False
                        else:
                            mining = True
                # Path finding
                if mining is False:
                    dest = location.map_location() #bc.MapLocation(bc.Planet.Earth, earthMap.width, earthMap.height)
                    fuzzygoto(unit, dest)
                    # Blueprint and build
                    d = random.choice(directions[1:])
                    if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                        gc.blueprint(unit.id, bc.UnitType.Factory, d)
                    if location.is_on_map():
                        nearby = gc.sense_nearby_units(location.map_location(), 2)
                        for other in nearby:
                            if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                                gc.build(unit.id, other.id)
                        break
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
