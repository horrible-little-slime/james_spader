import re

from drop_permutation import DropPermutation
def get_monsters():
    monster_file = open("monsters.txt")
    monsters = {}
    DROP_PATTERN = re.compile("(.+) \(\d+\)$")
    for line in monster_file:
        if line[0] == "#":
            continue
        data = line.replace("\n","").split("	")
        name = data[0].strip()
        drops = []
        for drop in range(4, len(data)):
            item_name_match = DROP_PATTERN.match(data[drop])
            if item_name_match:
                drops.append(item_name_match.group(1).replace("\n", "").strip())
        
        if len(drops) > 1:
            monsters[name] = drops
    return monsters
