# Lets convert old token file for Pokemon 3D to a new json-file
# Author: Daniel S. Billing (DanielRTRD)
# Github: https://github.com/DanielRTRD

import os, json

# File operations
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
tokens_en = os.path.join(THIS_FOLDER, "Tokens_en.dat")
json_en = os.path.join(THIS_FOLDER, "en.json")
oldTokenFile = open(tokens_en, "r")
oldTokenLines = oldTokenFile.readlines()

# Counted Lines
count = 0

# Predefine some groups
data = {}
data["language_name"] = ""
data_global = data["global"] = {}
data_regions = data["regions"] = {}
data_places = data["places"] = {}
data_pokemon = data["pokemon"] = {}
data_pokemon_name = data_pokemon["name"] = {}
data_pokemon_type = data_pokemon["type"] = {}
data_pokemon_move = data_pokemon["move"] = {}

# Read each line from the old token file and create a new data dict
for line in oldTokenLines:
    count += 1
    line = line.strip() # Strips the newline character

    if line.startswith("language_name"):
        data["language_name"] = line.split(",", 1)[1]
    elif line.startswith("global_"):
        if line.startswith("global_pokemon_type_"):
            key = line.split(",", 1)[0].replace("global_pokemon_type_", "")
            value = line.split(",", 1)[1]
            data_pokemon_type[key] = value
        elif line.startswith("global_pokemon_move_"):
            key = line.split(",", 1)[0].replace("global_pokemon_move_", "")
            value = line.split(",", 1)[1]
            data_pokemon_move[key] = value
        else:
            key = line.split(",", 1)[0].replace("global_", "")
            value = line.split(",", 1)[1]
            data_global[key] = value
    elif line.startswith("pokemon_name"):
        key = line.split(",", 1)[0].replace("pokemon_name_", "")
        value = line.split(",", 1)[1]
        data_pokemon_name[key] = value
    elif line.startswith("places"):
        key = line.split(",", 1)[0].replace("places_", "")
        value = line.split(",", 1)[1]
        data_places[key] = value
    elif line.startswith("johto") or line.startswith("kanto") or line.startswith("sevii_islands"):
        key = line.split(",", 1)[0]
        value = line.split(",", 1)[1]
        data_regions[key] = value
    elif "," in line:
        key = line.split(",", 1)[0]
        nameFixes = ["press_start", "add_server", "pause_menu", "new_game", "menu_bag", "offline_game", "map_screen", "trainer_card", "game_message", "party_screen"]
        if [ele for ele in nameFixes if(ele in key)]:
            name = key.split("_", 2)
            group = name[0] + "_" + name[1]
        else:
            group = key.split("_", 1)[0]
        if group not in data:
            data[group] = {}
        key = key.replace(group + "_", "")
        value = line.split(",", 1)[1]
        data[group][key] = value
    newLine = line.split("_", 1)

# Write new dict to new json-file
with open(json_en, "w") as outfile:
    json.dump(data, outfile, indent=4)

# Print the data for debugging purposes
#print(data)

# Print result
print("Converted {} lines!".format(count))
