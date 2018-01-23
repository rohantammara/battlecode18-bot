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
born_to_mine = []
born_to_build = []
blocked =  {}
workers = []
dukan = []
temp = []
blueprint_number=0

print("TestStarter")
factory_number=0

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(my_team)

def lay_blueprint(worker_id):
    for d in [bc.Direction.Northeast,bc.Direction.Northwest,bc.Direction.Southeast,bc.Direction.Southwest]:
        if  gc.can_blueprint(worker_id , bc.UnitType.Factory ,d):
            gc.blueprint(worker_id, bc.UnitType.Factory ,d)
            break
        else:
            continue
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
        for i in [1,2,3,4,5]:
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
        if gc.can_move(unit.id,d):
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
                     continue
            for values in blocked[unit.id]:
                if values == d:
                    stinky = True
                    break
                else:
                    stinky = False
            if stinky == False:
                gc.move_robot(unit.id,d)

                break

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
corner1= bc.MapLocation(bc.Planet.Earth,(earthMap.width),(earthMap.height))
corner2= bc.MapLocation(bc.Planet.Earth,0,(earthMap.height))
corner3= bc.MapLocation(bc.Planet.Earth,(earthMap.width),0)
corner4= bc.MapLocation(bc.Planet.Earth,0,0)
corners = [corner1,corner2,corner3,corner4]
while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location

            if gc.round()==1:
                born_to_mine.append(unit.id)
                for d in directions:
                    if gc.can_replicate(unit.id,d):
                        gc.replicate(unit.id,d)
                    else:
                        continue

            elif gc.round() ==2:
                if unit.id not in born_to_mine:
                    born_to_build.append(unit.id)
# Append workers

            if unit.id not in workers:
                workers.append(unit.id)
            if unit.unit_type == bc.UnitType.Worker :
# Append in Born_to_mine
                if not unit.id in born_to_mine and not unit.id in born_to_build:
                    born_to_mine.append(unit.id)

# Workers in Born_to_mine
                if unit.id in born_to_mine:
                    mining = Karbonite_Mining(unit.id,directions,unit,mining)
                    if mining == False:
                            born_to_mine.remove(unit.id)
                            if len(born_to_mine) == 0:
                                mining = False
                            else:
                                mining = True

# Workers in Born_to_build
                else:
                    for d in list(bc.Direction):
                        if gc.can_harvest(unit.id, d):
                            gc.harvest(unit.id, d)
                            break
                    nearby = gc.sense_nearby_units(location.map_location(), 2)
                    for other in nearby:
                        if other.unit_type == bc.UnitType.Factory:
                            if other.structure_is_built() and not other.id in dukan:
                                print("structure is built")
                                temp.append(other.id)
                            elif gc.can_build(unit.id,other.id):
                                gc.build(unit.id, other.id)
                            elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                 gc.repair(unit.id,other.id)
                    if gc.karbonite() >200 and gc.round()%20==0:
                        lay_blueprint(unit.id)
                    dukan.append(temp)
                    temp.clear()

                if unit.unit_type == bc.UnitType.Factory :
                    garrison = unit.structure_garrison()
                    if len(garrison)>0:
                        for d in directions:
                            if gc.can_unload(unit.id,d):
                                print("unloaded something")
                                gc.unload(unit.id,d)
                                continue

                    elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                        gc.produce_robot(unit.id, bc.UnitType.Knight)
                        print('produced a knight!')
                        continue

                if  unit.unit_type == bc.UnitType.Knight :
                    close_by=gc.sense_nearby_units(unit.map_location(),30)
                    for enemy in close_by:
                        if enemy.team !=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,enemy.id):
                            print("attacking a thing")
                            gc.attack(unit.id,other.id)
                            continue
                        else:
                            if (location.map_location().direction_to(centre) != bc.Direction.Center):
                                fuzzygoto(unit,centre)
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
