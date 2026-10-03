import json

json_data = {}

with open("dirt.json", "r") as file:
    json_data = json.loads(file.read())

files = [
        "dirt.txt",
        "dirt.json",
        "dirt.js",
        "dirt.py",
        "dirt.php",
        "dirt.html",
        "load-file.php",
        "save-file.php",
        "delete-file.php",
        "list-files.php",
        "list-branches.php",
        "delete-branch.php",
        "create-branch.php",
        "php.js",
        "php.html",
        "feed.html",
        "feed.js",
        "feed.css",
        "feed.json",
        "wall.html",
        "wall.txt",
        "README.md",
        "readme.html",
        "icon.html",
        "icon.json",
        "icon.txt"
]

json_data['files'] = files

with open("dirt.json", "w") as file:
    file.write(json.dumps(json_data, indent=4))

text = ""

for filename in files:
    text = text + "<" + filename + ">\n";
    with open(filename, "r") as file:
        text = text + file.read()
    text = text + "</" + filename + ">\n";
    
text_array = text.split("\n")

comment_text = ""
for line in text_array:
    comment_text += "#" + line + "\n"

with open("spore.py", "r") as file:
    spore_code =  file.read()

with open("dirtspore.py", "w") as file:
    file.write(spore_code + "\n#spore-break\n" + comment_text)
    