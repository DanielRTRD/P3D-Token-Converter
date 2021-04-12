# Lets convert old token file for Pokemon 3D to a new json-file
# Author: Daniel S. Billing (DanielRTRD)
# Github: https://github.com/DanielRTRD

import os, json

lang = "en"

# File operations
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
tokensFile = os.path.join(THIS_FOLDER, "Tokens_" + lang + ".dat")
jsonFile = os.path.join(THIS_FOLDER, lang + ".json")
oldTokenFile = open(tokensFile, "r")
oldTokenLines = oldTokenFile.readlines()

# Counted Lines
count = 0

# Predefine some groups
data = {}
data["language_name"] = ""
data_tokens = data["tokens"] = {}
data_global = data_tokens["global"] = {}
data_regions = data_tokens["regions"] = {}
data_places = data_tokens["places"] = {}
data_pokemon = data_tokens["pokemon"] = {}
data_pokemon_name = data_pokemon["name"] = {}
data_pokemon_type = data_pokemon["type"] = {}
data_pokemon_move = data_pokemon["move"] = {}

# Read each line from the old token file and create a new data dict
for line in oldTokenLines:
    count += 1
    line = line.strip() # Strips the newline character

    # Some saved languages has wierd chars on start of file, so we just check if line has the text instead of starting with
    if "language_name" in line:
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
        if group not in data_tokens:
            data_tokens[group] = {}
        key = key.replace(group + "_", "")
        value = line.split(",", 1)[1]
        data_tokens[group][key] = value
    newLine = line.split("_", 1)

# Write new dict to new json-file
with open(jsonFile, "w") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

# Print the data for debugging purposes
#print(data)

# Print result
print("Converted {} lines!".format(count))
