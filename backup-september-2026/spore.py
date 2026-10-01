with open("dirt.txt", "r") as file:
    dirt = file.read()

dirt_array = dirt.split("\n")
raw_dirt = ""
for line in dirt_array:
    raw_dirt += line[1:] + "\n"

js = raw_dirt.split("<dirt.js>")[1].split("</dirt.js>")[0]
html = raw_dirt.split("<dirt.html>")[1].split("</dirt.html>")[0]
py = raw_dirt.split("<dirt.py>")[1].split("</dirt.py>")[0]
php = raw_dirt.split("<dirt.php>")[1].split("</dirt.php>")[0]

with open("dirt.js", "w") as file:
    file.write(js)
with open("dirt.html", "w") as file:
    file.write(html)
with open("dirt.py", "w") as file:
    file.write(py)
with open("dirt.php", "w") as file:
    file.write(php)
