with open("dirt.txt", "r") as file:
    dirt = file.read()

js = dirt.split("<dirt.js>")[1].split("</dirt.js>")[0]
html = dirt.split("<dirt.html>")[1].split("</dirt.html>")[0]
py = dirt.split("<dirt.py>")[1].split("</dirt.py>")[0]
php = dirt.split("<dirt.php>")[1].split("</dirt.php>")[0]

with open("dirt.js", "w") as file:
    file.write(js)
with open("dirt.html", "w") as file:
    file.write(html)
with open("dirt.py", "w") as file:
    file.write(py)
with open("dirt.php", "w") as file:
    file.write(php)
