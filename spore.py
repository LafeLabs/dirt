import json
with open("dirtspore.py", "r") as file:
    dirtspore = file.read()

dirt = dirtspore.split("#spore-break")[2]

dirt_array = dirt.split("\n")
raw_dirt = ""
for line in dirt_array:
    raw_dirt += line[1:] + "\n"
json_text = raw_dirt.split("<dirt.json>")[1].split("</dirt.json>")[0]

json_data = json.loads(json_text)
file_names = json_data['files']

for file_name in file_names:
    file_text = raw_dirt.split("<" + file_name +">")[1].split("</" + file_name +">")[0]
    with open(file_name, "w") as file:
        file.write(file_text)
