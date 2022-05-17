import json
import os
import re
from drop_permutation import DropPermutation

from mafia_scraper import get_monsters

MAKE_SKILL_PATTERN = lambda username, skillname: re.compile("Round \d+: %s casts %s!" % (username, skillname.upper()))
danger_skills = ["emit duplicating drones", "\%FN, spit on them!", "duplicate", "feel nostalgia"]
DRONE_PATTERN = re.compile("After Battle: One of the matter duplicating drones seems to coalesce around the ")
ENCOUNTER_START_PATTERN = re.compile("Encounter: (.+)")
ITEM_DROP_PATTERN = re.compile("You acquire an item: (.+)")
random_drop_messages = ["You see a weird thing out of the corner of your eye, and you grab it. Far out, man!", ".+ looks up at you guiltily before disgorging a piece of equipment.", "You notice something valuable hidden", "You remember a party at KoL Con V, and you remember that you forgot to unpack your bags when you got home", "You think back on KoL Con V, when .+ gave you that delicious drink", "You remember that time at KoL Con V, when .+ bought you dinner.", "Something falls out of your can of mixed everything."]
RANDOM_DROP_PATTERN = re.compile("(?:" + ")|(?:".join(random_drop_messages) + ")")
monsters = get_monsters()
tracked_monsters = {}

def spade_log(path):
    player = path.split('_')[0]
    log = open(path, "r")

    SKILL_PATTERNS = [MAKE_SKILL_PATTERN(player, skillname) for skillname in danger_skills]
    ABC_PATTERN = re.compile("%s uses the Daily Affirmation: Always be Collecting!" % player)
    def is_dangerous_line(line): 
        for pattern in SKILL_PATTERNS:
            if pattern.match(line):
                return True
        return bool(DRONE_PATTERN.match(line)) or bool(ABC_PATTERN.match(line))

    current_encounter = ""
    is_dangerous = False
    current_drops = []
    ignore_next_line = False
    fight_over = False
    for line in log:
        name_match = ENCOUNTER_START_PATTERN.match(line)
        if name_match:
            current_encounter = name_match.group(1).replace("\n", "").strip()

        elif current_encounter and is_dangerous_line(line):
            is_dangerous = True
        
        if RANDOM_DROP_PATTERN.match(line):
            ignore_next_line = True
        
        if re.compile("Round \d+: %s wins the fight!" % player).match(line):
            fight_over = True

        else:
            item_match = ITEM_DROP_PATTERN.search(line)
            if item_match and fight_over and not ignore_next_line:
                item = item_match.group(1).replace("\n", "").strip()
                current_drops.append(item)

            elif (not re.compile(".").match(line)):
                if not is_dangerous and monsters.get(current_encounter):
                    if not tracked_monsters.get(current_encounter):
                        tracked_monsters[current_encounter] = DropPermutation(current_encounter, monsters[current_encounter])
                    tracked_monsters[current_encounter].filter_options(current_drops)
                is_dangerous = False
                current_encounter = ""
                fight_over = False
                current_drops = []
        ignore_next_line = False
os.chdir(".\\logs")
for name in os.listdir("."):
    spade_log(name)
os.chdir("..")
open("james_spader_results.JSON", "w").write(json.dumps({key: value.orders for (key, value) in tracked_monsters.items() if len(value.orders) == 1}))
open("james_spader_skipped_monsters.JSON", "w").write(json.dumps(DropPermutation.too_big_skipped))

