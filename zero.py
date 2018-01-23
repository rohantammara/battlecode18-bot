import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

#print("Test starting")

gc = bc.GameController()
# Initializing code
all_map_directions = [bc.Direction.Center, bc.Direction.North, bc.Direction.Northeast, bc.Direction.East,
bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest,
bc.Direction.West, bc.Direction.Northwest]

directions = [bc.Direction.North, bc.Direction.Northeast,
            bc.Direction.East, bc.Direction.Southeast, bc.Direction.South,
            bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,-7,-2,-6]
mining = True # Should the worker mine
corpus = []
miners = 0
prev_dir = bc.Direction.Center
earthMap = gc.starting_map(bc.Planet.Earth)
worker_number = 0
dukan = []
amadhya = []
knights = []
centre = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)
#print("TestStarter")

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

def Karbonite_Mining(id,directions,prev_dir,unit):
    karbonite_collected = False
    for d in all_map_directions:
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
            if gc.karbonite_at(loc) != 0 and gc.is_move_ready(id):
                mining = True
                fuzzygoto(unit,loc)
                break
            else:
                mining = False
    return (prev_dir)

def rotate(dir,amount):
    ind = directions.index(dir)
    return directions[(ind+amount)]
# Pathfinding
def fuzzygoto(unit,dest):
    toward = unit.location.map_location().direction_to(dest)
    for tilt in  tryRotate:
        d = rotate(toward,tilt)
        if gc.can_move(unit.id,d):
            gc.move_robot(unit.id,d)
            break

def lay_blueprint(unit):
    for d in directions:
        if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
            gc.blueprint(unit.id, bc.UnitType.Factory, d)
        else:
            continue

while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location
            replications = 0
            if gc.round() == 1:
                start_node = location.map_location()
                enemy_start = invert(start_node)
            ### Workers ###
            if unit.unit_type == bc.UnitType.Worker:
                # Replication
                if replications<3 and gc.karbonite()>70 and worker_number<10 and (gc.round())%15==0:
                    for d in directions:
                        if gc.can_replicate(unit.id,d):
                            gc.replicate(unit.id,d)
                            replications += 1
                            worker_number += 1
                        else:
                            continue
                # Mining
                if not unit.id in corpus and miners<4:
                    corpus.append(unit.id)
                    miners+=1

                if mining==True and unit.id in corpus:
                    prev_dir = Karbonite_Mining(unit.id,directions,prev_dir,unit)

                if mining == False:
                    corpus.remove(unit.id)
                    miners-=1

                if len(corpus) == 0:
                    mining = False
                else:
                    mining = True

                if not unit.id in corpus: #and bc.Unit.worker_has_acted()==False:
                    nearby = gc.sense_nearby_units(location.map_location(), 2)
                    for other in nearby:
                        if gc.can_build(unit.id,other.id):# and bc.Unit.worker_has_acted()==False:
                            gc.build(unit.id, other.id)
                            if bc.Unit.structure_is_built(other):
                                print("built a factory")

                            elif gc.can_repair(unit.id,other.id) and (other.health < other.max_health):# and bc.Unit.worker_has_acted()==False:
                                gc.repair(unit.id,other.id)
                                print("repaired a factory")
                                continue
                            elif gc.karbonite()>200 and len(dukan)<5 and gc.round()%20==0:
                                lay_blueprint(unit.id)

                            else:
                                direction_to_start_node=unit.location.map_location().direction_to(centre)
                                ind_for_this=directions.index(direction_to_start_node)
                                i=0
                                for tilt in  tryRotate:
                                    d = rotate(directions[ind_for_this - 4],tilt)
                                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id):
                                        gc.move_robot(unit.id,d)
                                        break
            ### Factory Output ###
            if unit.unit_type == bc.UnitType.Factory:
                if not unit.id in dukan:
                    dukan.append(unit.id)

                garrison = unit.structure_garrison()
                if len(garrison)>0:
                    for d in directions:
                        if gc.can_unload(unit.id,d):
                            gc.unload(unit.id,d)

                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight) and len(knights)<5:
                    print(len(knights))
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')

                elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger) and len(amadhya)<5:
                    gc.produce_robot(unit.id, bc.UnitType.Ranger)
                    print('produced a ranger!')
            ### Knights ###
            if  unit.unit_type == bc.UnitType.Knight :
                if not unit.id in knights:
                    knights.append(unit.id)

                if location.is_on_map():
                    close_by=gc.sense_nearby_units(location.map_location(), 2)
                    for enemy in close_by:
                        if enemy.team !=my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,enemy.id) :
                            print("attacking a thing")
                            gc.attack(unit.id,enemy.id)
                            break
                        else:
                            continue
                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(centre)!= bc.Direction.Center:
                            fuzzygoto(unit,centre)
            ### Rangers ###
            if  unit.unit_type == bc.UnitType.Ranger :
                if not unit.id in amadhya:
                    amadhya.append(unit.id)
                    print(len(amadhya))

                if location.is_on_map():
                    close_by_for_ranger= gc.sense_nearby_units(location.map_location(), 50)
                    for junta in close_by_for_ranger:
                        if junta.team != my_team and  gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, junta.id) :
                            print("attacking a thing")
                            gc.attack(unit.id, junta.id)
                            break
                        else:
                            continue

                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(centre)!= bc.Direction.Center :
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
