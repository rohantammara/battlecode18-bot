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
blueprint_number=0
legion_of_knights=[]
amadhya=[]

print("TestStarter")
factory_number=0

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(my_team)

def invert(loc):
    newx=earthMap.width-loc.x
    newy=earthMap.height-loc.y
    return bc.MapLocation(bc.Planet.Earth,newx,newy)
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
while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location

            if gc.round()==1:
                start_Node=location.map_location()
                enemy_start=invert(start_Node)
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
                                continue
                            elif gc.can_build(unit.id,other.id):
                                gc.build(unit.id, other.id)
                            elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                 gc.repair(unit.id,other.id)
                    if gc.karbonite() >200:
                        lay_blueprint(unit.id)
## SHREY'S CODE AFTER THIS!
            if unit.unit_type == bc.UnitType.Factory :
                garrison = unit.structure_garrison()
                if len(garrison)>0:
                    for d in directions:
                        if gc.can_unload(unit.id,d):
                            gc.unload(unit.id,d)

                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight) and len(legion_of_knights)<5:
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')

                elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger) and len(amadhya)<5:
                        gc.produce_robot(unit.id, bc.UnitType.Ranger)
                        print('produced a ranger!')

            if  unit.unit_type == bc.UnitType.Knight :

                if not unit.id in legion_of_knights:
                    legion_of_knights.append(unit.id)

                if location.is_on_map():
                    close_by = gc.sense_nearby_units(location.map_location(),2)
                    for enemy in close_by:
                        if enemy.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,enemy.id) :
                            print("attacking a thing")
                            gc.attack(unit.id,enemy.id)
                            break
                        else:
                            continue
                    if gc.is_move_ready(unit.id) and location.map_location().direction_to(enemy_start)!= bc.Direction.Center:
                        fuzzygoto(unit,enemy_start)

            if  unit.unit_type == bc.UnitType.Ranger :

                if not unit.id in amadhya:
                    amadhya.append(unit.id)


                if location.is_on_map():
                    close_by_for_ranger= gc.sense_nearby_units(location.map_location(),50)
                    for junta in close_by_for_ranger:
                        if junta.team !=my_team and  gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,junta.id) :
                            print("attacking a thing")
                            gc.attack(unit.id,junta.id)
                            break
                        else:
                            continue

                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(enemy_start)!= bc.Direction.Center :
                            fuzzygoto(unit,enemy_start)
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
