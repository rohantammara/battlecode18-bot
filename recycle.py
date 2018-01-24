
############### Shrey's worker code ##########################
        if replications<3 and gc.karbonite()>70 and worker_number<10 and (gc.round())%15==0:
            for d in directions:
                if gc.can_replicate(unit.id,d):
                    gc.replicate(unit.id,d)
                else:
                    continue

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
        # Blueprint and build
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
                    lay_blueprint(unit.id, bc.UnitType.Factory)

                else:
                    direction_to_start_node=unit.location.map_location().direction_to(centre)
                    ind_for_this=directions.index(direction_to_start_node)
                    i=0
                    for tilt in  tryRotate:
                        d = rotate(directions[ind_for_this - 4],tilt)
                        if gc.can_move(unit.id,d) and gc.is_move_ready(unit.id):
                            gc.move_robot(unit.id,d)
                            break
########################################################################
