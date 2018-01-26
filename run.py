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
#variablles for workers
earthMap =  gc.starting_map(bc.Planet.Earth)
centre= bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)
unit_needing_backup=[]
mining =  True
enemy_sensed=False
miners_on_mars = []
miners_on_mars_loc = []
born_to_mine = []
born_to_build = []
blocked =  {}
workers = []
dukan = [] #for factories
legion_of_knights=[] #for knights
#variables for rangers
number_enemy_sensed=[]
enemy_sensed=False
amadhya=[]
amadhya_on_mars = []
the_lone_ranger=[]
got_to_enemy_start=False
the_nights_watch=[]
mages=[]
pants=[]
maploc=[]
mars_maploc=[]
marsMap = gc.starting_map(bc.Planet.Mars)
enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height))
print("TestStarter")
ark_angels=[]
random.seed(1047)
temp = []
## A list of all passable locations on mars ## #what does this do
i = 0
while i< marsMap.width:
    j=0
    while j < marsMap.height:
        loc = bc.MapLocation(bc.Planet.Mars, i, j)
        if marsMap.is_passable_terrain_at(loc):
            mars_maploc.append(loc)
        j+=1
    i+=1
random.shuffle(mars_maploc)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(my_team)
def does_it_need_backup(close_by,unit):
    for junta in close_by:
        if junta.team!=my_team:
            number_enemy_sensed.append(junta.id)
    if len(number_enemy_sensed)>2:
        backup=True
    else:
        backup=False

def knights_job(unit):
    if location.is_on_map():
        close_by = gc.sense_nearby_units(location.map_location(),2)
        for enemy in close_by:
            if enemy.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,enemy.id) :
                print("attacking a thing")
                gc.attack(unit.id,enemy.id)
                break
            else:
                continue
        if gc.is_move_ready(unit.id) and location.map_location().direction_to(centre)!= bc.Direction.Center:
            fuzzygoto(unit,centre)
        if unit.health==0:
            legion_of_knights.remove(unit.id)

def rangers_job(unit,got_to_enemy_start,enemy_sensed):

    if location.is_on_planet(bc.Planet.Earth):
        if amadhya.index(unit.id) == 0:
            if pos == 'Top' or pos == 'Bottom':
                if location.map_location().y != corner1.y:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner1) != bc.Direction.Center:
                        fuzzygoto(unit,corner1)
            elif pos == 'Left' or pos == 'Right':
                if location.map_location().x != corner1.x:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner1) != bc.Direction.Center:
                        fuzzygoto(unit,corner1)

        elif amadhya.index(unit.id) == 1:
            if pos == 'Top' or pos == 'Bottom':
                if location.map_location().y != corner2.y:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner2) != bc.Direction.Center:
                        fuzzygoto(unit,corner2)

            elif pos == 'Left' or pos == 'Right':
                if location.map_location().x != corner2.x:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner2) != bc.Direction.Center:
                        fuzzygoto(unit,corner2)

        elif amadhya.index(unit.id) == 2:
            if pos == 'Top' or pos == 'Bottom':
                if location.map_location().y != corner3.y:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner3) != bc.Direction.Center:
                        fuzzygoto(unit,corner3)

            elif pos == 'Left' or pos == 'Right':
                if location.map_location().x != corner3.x:
                    if gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(corner3) != bc.Direction.Center:
                        fuzzygoto(unit,corner3)

    elif location.is_on_planet(bc.Planet.Mars):
        if unit.id not in amadhya_on_mars and len(amadhya_on_mars) < 5:
            amadhya_on_mars.append(unit.id)
        if unit.id in amadhya_on_mars:
            ind = amadhya_on_mars.index(unit.id)
            fuzzygoto(unit,miners_on_mars_loc[ind])
    backup=False
    dont_move=False
    if location.is_on_map():
        close_by_for_ranger= gc.sense_nearby_units(location.map_location(),70)

        backup=does_it_need_backup(close_by_for_ranger,unit)

        if unit in unit_needing_backup and backup==False:
            unit_needing_backup.remove(unit)
        elif not unit in unit_needing_backup and backup==True:
            unit_needing_backup.append(unit)


        for junta in close_by_for_ranger:
            if not junta:
                dont_move=False
            elif junta.team!=my_team and unit.location.map_location().is_within_range(50,junta.location.map_location()):
                dont_move=True
            if junta.team !=my_team and  gc.is_attack_ready(unit.id) and gc.can_attack(unit.id,junta.id) :
                #print("attacking a thing")
                current_junta_health=junta.health
                print('junta.id',junta.id)
                gc.attack(unit.id,junta.id)
                print('junta.health', junta.health)

                break

        if not unit in the_nights_watch and len(the_nights_watch)<3:
            the_nights_watch.append(unit)

        if unit_needing_backup:

            fuzzygoto(unit,unit_needing_backup[0].location.map_location())

def invert(loc):
    newx=earthMap.width-loc.x
    newy=earthMap.height-loc.y
    return bc.MapLocation(bc.Planet.Earth,newx,newy)

def lay_blueprint(worker_id, structure):
    for d in [directions[1], directions[3], directions[5],directions[7]]:
        if gc.can_blueprint(worker_id, structure, d):
            gc.blueprint(worker_id, structure, d)
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

while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location

            if gc.round()==1:
                start_node=location.map_location()
                enemy_start=invert(start_node)

# Append workers

            if unit.unit_type == bc.UnitType.Worker :
                if location.is_on_map():
                    if unit.id not in workers:
                        workers.append(unit.id)

# Append in Born_to_mine
                    if gc.round()==1:
                        born_to_mine.append(unit.id)
                        for d in directions:
                            if gc.can_replicate(unit.id,d):
                                gc.replicate(unit.id,d)
                            else:
                                continue

                        if start_node.y < earthMap.height//2: # find out whether in top or bottom
                            if 'Bottom' not in maploc:
                                maploc.append('Bottom')
                        if start_node.y > earthMap.height//2:
                            if 'Top' not in maploc:
                                maploc.append('Top')

                    elif gc.round() ==2:
                        if unit.id not in born_to_mine:
                            born_to_build.append(unit.id)

                        if len(maploc) == 1: # find out whether in left or right
                            pos = maploc[0]
                        else:
                            if start_node.x < earthMap.width//2:
                                if 'Left' not in temp:
                                    temp.append('Left')
                            if start_node.x > earthMap.width//2:
                                if 'Right' not in temp:
                                    temp.append('Right')

                    elif gc.round() ==3:
                            if len(temp)== 1:
                                pos = temp[0]
                            elif len(temp) ==2:
                                pos ='Opposite'
                            temp.clear()

                            if pos == 'Bottom':
                                corner1 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//4,(earthMap.height)//3)
                                corner2 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//2,(earthMap.height)//3)
                                corner3 = bc.MapLocation(bc.Planet.Earth, 3*(earthMap.width)//4,(earthMap.height)//3)
                                enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height))
                            elif pos == 'Top':
                                corner1 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//4,2*(earthMap.height)//3)
                                corner2 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//2,2*(earthMap.height)//3)
                                corner3 = bc.MapLocation(bc.Planet.Earth, 3*(earthMap.width)//4,2*(earthMap.height)//3)
                                enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,0)
                            elif pos == 'Left':
                                corner1 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//3,(earthMap.height)//4)
                                corner2 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//3,(earthMap.height)//2)
                                corner3 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//3,3*(earthMap.height)//4)
                                enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width),(earthMap.height)//2)
                            elif pos == 'Right':
                                print(pos)
                                corner1 = bc.MapLocation(bc.Planet.Earth, 2*(earthMap.width)//3,(earthMap.height)//4)
                                corner2 = bc.MapLocation(bc.Planet.Earth, 2*(earthMap.width)//3,(earthMap.height)//2)
                                corner3 = bc.MapLocation(bc.Planet.Earth, 2*(earthMap.width)//3,3*(earthMap.height)//4)
                                enemy_edge = bc.MapLocation(bc.Planet.Earth,0,(earthMap.height)//2)
                            else:
                                print(pos)
                                corner1 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//2,(earthMap.height)//2)
                                corner2 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//2,(earthMap.height)//2)
                                corner3 = bc.MapLocation(bc.Planet.Earth, (earthMap.width)//2,(earthMap.height)//2)
                                enemy_edge = bc.MapLocation(bc.Planet.Earth,(earthMap.width)//2,(earthMap.height)//2)

                    if not unit.id in born_to_mine and not unit.id in born_to_build:
                        born_to_mine.append(unit.id)

                    if location.is_in_garrison():
                        rocket_id = location.structure()
                        for d in directions:
                            if gc.can_unload(rocket_id,d):
                                gc.unload(rocket_id,d)
                                gc.disintegrate_unit(rocket_id)

                    if len(workers) < 20 and (gc.round())%5 == 0: # continue replication till sufficient
                        for d in directions:
                            if gc.can_replicate(unit.id,d):
                                gc.replicate(unit.id,d)
    # Workers in Born_to_mine
                    if unit.id in born_to_mine:
                        mining = Karbonite_Mining(unit.id,directions,unit,mining)
                        if mining == False:
                            born_to_mine.remove(unit.id)
                            if len(born_to_mine) == 0:
                                mining = False
                            else:
                                mining = True

                            if gc.planet()==bc.Planet.Earth and unit.location.map_location().direction_to(enemy_edge)!=bc.Direction.Center:
                                direction_to_start_node=unit.location.map_location().direction_to(enemy_edge)
                                ind_for_this=directions.index(direction_to_start_node)
                                print("got here")
                                for tilt in  tryRotate:
                                    d = rotate(directions[ind_for_this - 4],tilt)
                                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id):
                                        gc.move_robot(unit.id,d)
                                        break

                                if location.is_on_planet(bc.Planet.Mars):
                                    if unit.id not in miners_on_mars and len(miners_on_mars) < 5:
                                        miners_on_mars.append(unit.id)
                                        miners_on_mars_loc.append(location.map_location())
                                    elif unit.id in miners_on_mars:
                                        ind = miners_on_mars.index(unit.id)
                                        miners_on_mars_loc[ind] = location.map_location()
#miners need work
                                if location.is_on_map():
                                    nearby = gc.sense_nearby_units(location.map_location(), 2)
                                    for other in nearby:
                                        if other.unit_type == bc.UnitType.Factory:
                                            if other.structure_is_built() and not other.id in dukan:
                                                continue
                                            elif gc.can_build(unit.id,other.id):
                                                gc.build(unit.id, other.id)
                                            elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                                 gc.repair(unit.id,other.id)
                                        if other.unit_type == bc.UnitType.Rocket:
                                            if other.structure_is_built() and not other.id in pants:
                                                continue
                                            elif gc.can_build(unit.id, other.id):
                                                gc.build(unit.id, other.id)

    # Workers in Born_to_build
                    else:
                        for d in list(bc.Direction):
                            if gc.can_harvest(unit.id, d):
                                gc.harvest(unit.id, d)
                                break

                        if location.is_on_map():
                            nearby = gc.sense_nearby_units(location.map_location(), 2)
                            for other in nearby:
                                if other.unit_type == bc.UnitType.Factory:
                                    if other.structure_is_built() and not other.id in dukan:
                                        continue
                                    elif gc.can_build(unit.id,other.id):
                                        gc.build(unit.id, other.id)
                                    elif gc.can_repair(unit.id,other.id) and other.health<other.max_health:
                                         gc.repair(unit.id,other.id)

                                if other.unit_type == bc.UnitType.Rocket:
                                    if other.structure_is_built() and not other.id in pants:
                                        continue
                                    elif gc.can_build(unit.id, other.id):
                                        gc.build(unit.id, other.id)
                            if gc.karbonite() > 100 and len(pants)<4:
                                lay_blueprint(unit.id, bc.UnitType.Rocket)
                            if gc.karbonite() > 200 and len(dukan)<8:
                                lay_blueprint(unit.id, bc.UnitType.Factory)

### Rocket Science ###
            if unit.unit_type == bc.UnitType.Rocket:
                if not unit.id in pants:
                    pants.append(unit.id)
                if unit.health == 0:
                    pants.remove(unit.id)
                garrison = unit.structure_garrison()
                if len(garrison) == 0:
                    nearby = gc.sense_nearby_units(location.map_location(),2)
                    for robot in nearby:
                        if gc.is_move_ready(robot.id) and gc.can_load(unit.id, robot.id):
                            gc.load(unit.id, robot.id)
                            print('unit has been loaded!')
                elif len(garrison) != 0:
                    if location.is_on_planet(bc.Planet.Earth) and gc.current_duration_of_flight()<100:
                        for land in mars_maploc:
                            if gc.has_unit_at_location(land) == False and gc.can_launch_rocket(unit.id, land):
                                mars_maploc.remove(land)
                                gc.launch_rocket(unit.id, land)
                                print('a rocket has been launched!')
                    elif location.is_on_planet(bc.Planet.Mars):
                        print("I'm on Mars!")
                        for d in directions:
                            if gc.can_unload(unit.id,d):
                                gc.unload(unit.id,d)
## FACTORY ##
            if unit.unit_type == bc.UnitType.Factory :

                if not unit.id in dukan:
                    dukan.append(unit.id)

                garrison = unit.structure_garrison()
                if len(garrison)>0:
                    for d in directions:
                        if gc.can_unload(unit.id,d):
                            gc.unload(unit.id,d)
#producing knights
                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight) and len(legion_of_knights)<5:
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')
#producing rangers
                elif gc.can_produce_robot(unit.id, bc.UnitType.Ranger) and len(amadhya)<5:
                        gc.produce_robot(unit.id, bc.UnitType.Ranger)
                        print('produced a ranger!')


                elif gc.can_produce_robot(unit.id, bc.UnitType.Mage) and len(mages)<4:
                        gc.produce_robot(unit.id, bc.UnitType.Mage)
                        print('produced a mage!')

                elif gc.can_produce_robot(unit.id, bc.UnitType.Healer) and len(ark_angels)<4:
                        gc.produce_robot(unit.id, bc.UnitType.Healer)
                        print('produced a healer!')

            if  unit.unit_type == bc.UnitType.Healer :

                if not unit in ark_angels :
                    ark_angels.append(unit)

            if  unit.unit_type == bc.UnitType.Knight :

                if not unit.id in legion_of_knights:
                    legion_of_knights.append(unit.id)

                knights_job(unit)


            if  unit.unit_type == bc.UnitType.Ranger :

                if not unit.id in amadhya:
                    amadhya.append(unit.id)

                rangers_job(unit,got_to_enemy_start,enemy_sensed)

            if unit.unit_type == bc.UnitType.Mage :

                if not unit.id in mages:
                    mages.append(unit.id)
                    print(len(mages))

                if location.is_on_map():
                    close_by = gc.sense_nearby_units(location.map_location(), 30)
                    for athing in close_by:
                        if athing.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, athing.id):
                            gc.attack(unit.id, athing.id)
                            print('literally attacking a thing')
                            break
                        else:
                            continue

                    if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id) and unit.location.map_location().direction_to(bc.MapLocation(bc.Planet.Earth, unit.location.map_location().x, enemy_edge.y))!= bc.Direction.Center :
                            fuzzygoto(unit, bc.MapLocation(bc.Planet.Earth, unit.location.map_location().x, enemy_edge.y))

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
