import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

print("Test starting")

gc = bc.GameController()
directions = list(bc.Direction)
mining = True

print("TestStarter")

random.seed(1047)

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Mage)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(my_team)

while True:
    print('pyround:', gc.round())

    try:

        for unit in gc.my_units():
            location = unit.location
## Karbonite_Mining

            karbonite_collected = False
            if unit.unit_type == bc.UnitType.Worker:
                for d in directions:
                    if gc.can_harvest(unit.id, d):
                        gc.harvest(unit.id, d)
                        prev_dir = d
                        karbonite_collected = False
                        break
                    else:
                        karbonite_collected = True

                if  karbonite_collected == True and gc.is_move_ready(unit.id) and gc.can_move(unit.id, prev_dir):
                    gc.move_robot(unit.id, prev_dir)



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
