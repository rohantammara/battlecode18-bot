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
enemy_sensed=False
born_to_mine = []
born_to_build = []
blocked =  {}
workers = []
dukan = []
blueprint_number=0
legion_of_knights=[]
amadhya=[]
the_lone_ranger=[]
got_to_enemy_start=False
steps_north=0
steps_east=0
steps_west=0
steps_south=0
the_neighborhood_watch=[]

print("TestStarter")
factory_number=0

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
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
        for i in [5,10,17,26,37,50]:
            for loc in gc.all_locations_within(location.map_location(),i):
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
centre= bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)
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

# Workers in Born_to_build center
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

                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight) and len(legion_of_knights)<5 and (enemy_sensed==True or got_to_enemy_start==True):
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')

                elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                    if (enemy_sensed==False and got_to_enemy_start==False) and len(amadhya)<5:
                        gc.produce_robot(unit.id, bc.UnitType.Ranger)
                        print('produced a ranger!')
                    elif (enemy_sensed==True or got_to_enemy_start==True) and len(amadhya)<7:
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
                        fuzzygoto(unit,centre)
                    if unit.health==0:
                        legion_of_knights.remove(unit.id)

            if  unit.unit_type == bc.UnitType.Ranger :

                if not unit.id in amadhya:
                    amadhya.append(unit.id)


                if location.is_on_map():
                    close_by_for_ranger= gc.sense_nearby_units(location.map_location(),70)
                    for junta in close_by_for_ranger:
                        if junta.team !=my_team and  gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,junta.id) :
                            print("attacking a thing")
                            gc.attack(unit.id,junta.id)
                            break
                        elif not gc.can_attack(unit.id,junta.id) and unit.id in the_neighborhood_watch and junta.team !=my_team:
                            enemy_sensed=True
                            continue

                    if not unit.id in the_lone_ranger and len(the_lone_ranger)==0:
                        the_lone_ranger.append(unit.id)

                    if unit.id in the_lone_ranger:
                        if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(enemy_start)!= bc.Direction.Center and got_to_enemy_start==False :
                                fuzzygoto(unit,enemy_start)
                        if location.map_location().distance_squared_to(enemy_start)<20:
                            got_to_enemy_start=True

                    if not unit.id in the_lone_ranger and enemy_sensed==False and len(the_neighborhood_watch)<5:
                        the_neighborhood_watch.append(unit.id)

                    if unit.id in the_neighborhood_watch and gc.is_move_ready(unit.id):
                        if the_neighborhood_watch.index(unit.id)==0 and steps_north<5 and gc.can_move(unit.id,bc.Direction.North):
                            gc.move_robot(unit.id,bc.Direction.North)
                            steps_north+=1
                        elif  the_neighborhood_watch.index(unit.id)==1 and steps_east<5 and gc.can_move(unit.id,bc.Direction.East):
                            gc.move_robot(unit.id,bc.Direction.East)
                            steps_east+=1
                        elif the_neighborhood_watch.index(unit.id)==2 and steps_south<5 and gc.can_move(unit.id,bc.Direction.South):
                            gc.move_robot(unit.id,bc.Direction.South)
                            steps_south+=1
                        elif the_neighborhood_watch.index(unit.id)==3 and steps_west<5 and gc.can_move(unit.id,bc.Direction.West):
                            gc.move_robot(unit.id,bc.Direction.West)
                            steps_west+=1

                    if got_to_enemy_start==True:
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
