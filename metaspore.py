text = ""

text = text + "<dirt.js>\n";
with open("dirt.js", "r") as file:
    text = text + file.read()
text = text + "</dirt.js>\n";

text = text + "<dirt.py>\n";
with open("dirt.py", "r") as file:
    text = text + file.read()
text = text + "</dirt.py>\n";
    
text = text + "<dirt.php>\n";
with open("dirt.php", "r") as file:
    text = text + file.read()
text = text + "</dirt.php>\n";

text = text + "<dirt.html>\n";
with open("dirt.html", "r") as file:
    text = text + file.read()
text = text + "<dirt.html>\n";

text_array = text.split("\n")

comment_text = ""
for line in text_array:
    comment_text += "#" + line + "\n"

with open("spore.py", "r") as file:
    spore_code =  file.read()

with open("dirtspore.py", "w") as file:
    file.write(spore_code + "#spore-break\n" + comment_text)
    