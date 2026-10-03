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

#spore-break
#<dirt.txt>
#
#THE PURPOSE OF DIRT IS TO BUILD FULL STACK TRASH MAGIC
#THE PURPOSE OF TRASH MAGIC IS TO BUILD A GLOBAL NETWORK WHICH DELIVERS EVERYTHING FREE TO EVERYONE EVERYWHERE RIGHT NOW USING ONLY TRASH AND WHAT IS GROWN LOCALLY AND LOCAL ENERGY OF THE SUN, THE MOON, AND THE LIVING EARTH
#</dirt.txt>
#<dirt.json>
#{
#    "files": [
#        "dirt.txt",
#        "dirt.json",
#        "dirt.js",
#        "dirt.py",
#        "dirt.php",
#        "dirt.html",
#        "load-file.php",
#        "save-file.php",
#        "delete-file.php",
#        "list-files.php",
#        "list-branches.php",
#        "delete-branch.php",
#        "create-branch.php",
#        "php.js",
#        "php.html",
#        "feed.html",
#        "feed.js",
#        "feed.css",
#        "feed.json",
#        "wall.html",
#        "wall.txt",
#        "README.md",
#        "readme.html"
#    ]
#}</dirt.json>
#<dirt.js>
#
#const ws = new WebSocket('ws://localhost:8086');
#const pendingRequests = new Map();
#const messageQueue = [];
#let messageIdCounter = 0;
#
#ws.onopen = () => {
#    while (messageQueue.length > 0) {
#        const sendFn = messageQueue.shift();
#        sendFn();
#    }
#};
#
#ws.onmessage = (event) => {
#    try {
#        const response = JSON.parse(event.data);
#        const { id, success, data, error } = response;
#        if (pendingRequests.has(id)) {
#            const { resolve, reject } = pendingRequests.get(id);
#            pendingRequests.delete(id);
#            if (success) {
#                resolve(data);
#            } else {
#                reject(new Error(error || 'WebSocket request failed'));
#            }
#        }
#    } catch (e) {
#        console.error(e);
#    }
#};
#
#function sendWebSocketMessage(action, payload) {
#    return new Promise((resolve, reject) => {
#        const id = ++messageIdCounter;
#        pendingRequests.set(id, { resolve, reject });
#        const message = { id: id, action: action, ...payload };
#
#        const performSend = () => {
#            if (ws.readyState === WebSocket.OPEN) {
#                ws.send(JSON.stringify(message));
#            } else {
#                reject(new Error('WebSocket closed before sending'));
#            }
#        };
#
#        if (ws.readyState === WebSocket.OPEN) {
#            performSend();
#        } else if (ws.readyState === WebSocket.CONNECTING) {
#            messageQueue.push(performSend);
#        } else {
#            pendingRequests.delete(id);
#            reject(new Error('WebSocket is not open'));
#        }
#    });
#}
#
#function load_file(name) { 
#    return sendWebSocketMessage('load_file', { filename: name }); 
#} 
#
#function save_file(name, data) { 
#    return sendWebSocketMessage('save_file', { filename: name, data: data });
#} 
#
#function pull_file(url) { 
#    return sendWebSocketMessage('pull_file', { url: url}); 
#} 
#
#function push_file(dirt_php, file, data) { 
#    return sendWebSocketMessage('push_file', { dirt_php: dirt_php, file: file, data: data }); 
#} 
#function delete_file(name) { 
#    return sendWebSocketMessage('delete_file', { filename: name }); 
#} 
#
#function delete_branch(name) { 
#    return sendWebSocketMessage('delete_branch', { branch: name }); 
#} 
#
#function create_branch(name) { 
#    return sendWebSocketMessage('create_branch', { branch: name }); 
#}
#
#function list_files(fork) { 
#    return sendWebSocketMessage('list_files', { directory: fork || null }); 
#} 
#
#function list_branches() { 
#    return sendWebSocketMessage('list_branches', {}); 
#}
#</dirt.js>
#<dirt.py>
#
#import asyncio
#import json
#import os
#import shutil
#import websockets
#import urllib.request
#
#async def handle_client(websocket):
#    try:
#        async for message in websocket:
#            try:
#                request = json.loads(message)
#            except json.JSONDecodeError:
#                await send_error(websocket, None, "Invalid JSON format")
#                continue
#
#            msg_id = request.get("id")
#            action = request.get("action")
#
#            try:
#                if action == "load_file":
#                    filename = request.get("filename")
#                    if not filename:
#                        await send_error(websocket, msg_id, "Missing filename")
#                        continue
#                    
#                    if os.path.exists(filename) and os.path.isfile(filename):
#                        with open(filename, "r", encoding="utf-8") as f:
#                            content = f.read()
#                        await send_success(websocket, msg_id, content)
#                    else:
#                        await send_success(websocket, msg_id, "")
#
#                elif action == "save_file":
#                    filename = request.get("filename")
#                    data = request.get("data", "")
#                    if not filename:
#                        await send_error(websocket, msg_id, "Missing filename")
#                        continue
#                    
#                    with open(filename, "w", encoding="utf-8") as f:
#                        f.write(data)
#                    await send_success(websocket, msg_id, "File saved successfully")
#
#                elif action == "push_file":
#                    import urllib.parse
#                    dirt_php = request.get("dirt_php")
#                    filename = urllib.parse.quote(request.get("file", ""))
#                    data = urllib.parse.quote(request.get("data", ""))
#                    
#                    push_url = f"{dirt_php}?file={filename}&data={data}"
#                    
#                    def sync_push():
#                        with urllib.request.urlopen(push_url) as response:
#                            return response.read().decode('utf-8')
#                            
#                    server_response = await asyncio.to_thread(sync_push)
#                    await send_success(websocket, msg_id, "File pushed successfully")
#                
#                elif action == "pull_file":
#                    url = request.get("url")
#                    with urllib.request.urlopen(url) as response:
#                        content = response.read().decode('utf-8')
#                    await send_success(websocket, msg_id, content)
#                elif action == "delete_file":
#                    filename = request.get("filename")
#                    if not filename:
#                        await send_error(websocket, msg_id, "Missing filename")
#                        continue
#                    
#                    if os.path.exists(filename) and os.path.isfile(filename):
#                        os.remove(filename)
#                    await send_success(websocket, msg_id, "File deleted")
#
#                elif action == "delete_branch":
#                    branch = request.get("branch")
#                    if not branch:
#                        await send_error(websocket, msg_id, "Missing branch name")
#                        continue
#                    
#                    if os.path.exists(branch) and os.path.isdir(branch):
#                        shutil.rmtree(branch)
#                    await send_success(websocket, msg_id, "Branch deleted")
#
#                elif action == "list_files":
#                    directory = request.get("directory") or "."
#                    if os.path.exists(directory) and os.path.isdir(directory):
#                        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#                        await send_success(websocket, msg_id, files)
#                    else:
#                        await send_success(websocket, msg_id, [])
#
#                elif action == "list_branches":
#                    items = os.listdir(".")
#                    branches = [i for i in items if os.path.isdir(i)]
#                    await send_success(websocket, msg_id, branches)
#
#                elif action == "create_branch":
#                    branch = request.get("branch")
#                    if not branch:
#                        await send_error(websocket, msg_id, "Missing branch name")
#                        continue
#                    
#                    os.makedirs(branch, exist_ok=True)
#                    allowed_extensions = {'txt', 'html', 'css', 'js', 'json', 'php', 'md', 'sh', 'bat', 'ipynb', 'py'}
#                    
#                    for file in os.listdir("."):
#                        if os.path.isfile(file):
#                            ext = file.split(".")[-1].lower() if "." in file else ""
#                            if ext in allowed_extensions:
#                                shutil.copy(file, os.path.join(branch, file))
#                                
#                    await send_success(websocket, msg_id, "Branch created successfully")
#
#                else:
#                    await send_error(websocket, msg_id, f"Unknown action: {action}")
#
#            except Exception as e:
#                await send_error(websocket, msg_id, str(e))
#
#    except websockets.exceptions.ConnectionClosed:
#        pass
#
#async def send_success(websocket, msg_id, data):
#    response = {"id": msg_id, "success": True, "data": data}
#    await websocket.send(json.dumps(response))
#
#async def send_error(websocket, msg_id, error_message):
#    response = {"id": msg_id, "success": False, "error": error_message}
#    await websocket.send(json.dumps(response))
#
#async def main():
#    async with websockets.serve(handle_client, "0.0.0.0", 8086):
#        await asyncio.Future()
#
#if __name__ == "__main__":
#    try:
#        asyncio.run(main())
#    except KeyboardInterrupt:
#        pass</dirt.py>
#<dirt.php>
#
#<?php
#    $data = $_GET["data"]; //get data 
#    $filename = $_GET["file"];//get filename
#    $file = fopen($filename,"w");// create new file with this name
#    fwrite($file,$data); //write data to file
#    fclose($file);  //close file
#?></dirt.php>
#<dirt.html>
#
# <!doctype html>
#<html>
#<head>
# <!-- 
#edit files in .html, .js, .json, .css, .php, .py, .txt,  and .md
#-->
#
#    <link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/3gAA//8AAPb/AAD//wAA//8AAP/7AAD/3wAA3/8AAP7/AAD//wAA//8AAP93AADv/wAA//8AAP//AAB+/gAA" rel="icon" type="image/x-icon">
#    
#<!--
#ace.js project home:
#https://ace.c9.io/
#
#list of languages:
#https://cloud9-sdk.readme.io/docs/language-mode
#ace.js is BSD license
#
#-->    
#
#<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/ace.js"></script>
#<script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.js"></script>
#<script src = "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>   
#
#<script src="dirt.js"></script>
#<title>dirt code editor</title>
#</head>
#<body>
#
#<div id = "lightdarkbutton" class = "button">LIGHT MODE</div>
#
#<a href=  "index.html" style = "display:none;position:absolute;right:5px;top:1.5em;font-size:2em;font-family:Arial">HOME</a>
#
#
#<table id = "inputtable">
#    <tr>
#        <td>Current File Name:</td>
#        <td id = "currentfilename"></td>
#    </tr>
#    <tr>
#        <td>New File Name(end with .html, .js, .css, .py, .bat, .json, .php, .md, .txt):</td>
#        <td><input id = "newscrollinput"/></td>
#    </tr>
#</table>
#
#
#<div id="maineditor" contenteditable="true" spellcheck="false"></div>
#
#<div id="p5-canvas-container"></div>
#  
#<div id = "filescroll">
#</div>
#<script>
#
#
#editor = ace.edit("maineditor");
#editor.setTheme("ace/theme/github");
#//editor.setTheme("ace/theme/vibrant_ink");
#editor.getSession().setMode("ace/mode/html");
#editor.getSession().setUseWrapMode(true);
#editor.$blockScrolling = Infinity;
#editor.setTheme("ace/theme/vibrant_ink");
#editor.setOption("useWorker", false);
#
#
#currentFile = "dirt.html";
#
#
#load_file(currentFile).then(
#    filedata => {
#        setMode();
#        editor.setValue(filedata);
#        document.getElementById("currentfilename").innerHTML = currentFile;
#    }
#);
#
#
#scrolls = [];
#
#list_files().then(files => {
#    scrolls = files;
#    for(var index = 0;index < scrolls.length;index++) {    
#        if(scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".html" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".txt" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".css" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".php" || scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".js" ||scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".py" || scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".md" ||    scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".json"|| scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".bat"|| scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".sh"){
#     
#        if(scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".html"){
#            var newa = document.createElement("A");
#            newa.innerHTML = scrolls[index];
#            newa.href = scrolls[index];
#            document.getElementById("filescroll").appendChild(newa);
#         }             
#        var newscrollbutton = document.createElement("div");
#        newscrollbutton.classList.add("file");
#        newscrollbutton.classList.add("html");
#        if(scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".js"){
#            newscrollbutton.style.borderColor = "red";
#        }
#        if(scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".md"){
#            newscrollbutton.style.borderColor = "#0000ff80";
#        }
#        if(scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".css"){
#            newscrollbutton.style.borderColor = "yellow";
#        }
#        if(scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".php"){
#            newscrollbutton.style.borderColor = "purple";
#        }
#        newscrollbutton.innerHTML =  scrolls[index];
#        document.getElementById("filescroll").appendChild(newscrollbutton);
#        newscrollbutton.onclick = function(){
#            currentFile = this.innerHTML;
#            load_file(currentFile).then(
#                filedata => {
#                    setMode();
#                    editor.setValue(filedata);
#                    document.getElementById("currentfilename").innerHTML = currentFile;
#                    var fileType = currentFile.split("/")[0]; 
#                    var fileName = currentFile.split("/")[1];
#                    //document.getElementById("newscrollinput").value = fileName;
#                }
#            );
#
#        
#            document.getElementById("currentfilename").innerHTML = currentFile;
#            
#        }
#    
#        }
#    }
#
#});
#
#
#deleteMode = true;
#
#
#document.getElementById("currentfilename").innerHTML = currentFile;
#
#document.getElementById("maineditor").onkeyup = function(){
#    data = editor.getSession().getValue();
#    save_file(currentFile,data);
#    var fileType = currentFile.split("/")[0]; 
#    var fileName = currentFile.split("/")[1];
#}
#
#document.body.style.backgroundColor = "#202020";
#document.body.style.color = "white";
#document.getElementById("newscrollinput").style.backgroundColor = "#202020";
#document.getElementById("newscrollinput").style.color = "white";        
#
#editor.setTheme("ace/theme/vibrant_ink");
#
#
#
#document.getElementById("newscrollinput").value = "";
#
#name = "";
#document.getElementById("newscrollinput").onchange = function(){
#    name = this.value;
#    currentFile = name;
#    scroll = editor.getSession().getValue();
#    setMode();
#    editor.setValue(scroll);  
#    data = scroll;
#
#    save_file(currentFile,data);
#
#
#    addcodelink(name);
#    document.getElementById("currentfilename").innerHTML = currentFile;
#
#}
#
#
#function addcodelink(codename){
#    var newscrollbutton = document.createElement("div");
#    newscrollbutton.classList.add("file");
#    newscrollbutton.classList.add("html");
#    newscrollbutton.innerHTML = codename;
#    document.getElementById("filescroll").appendChild(newscrollbutton);
#    newscrollbutton.onclick = function(){
#        currentFile = this.innerHTML;
#        //use php script to load current file;
#
#
#        load_file(currentFile).then(
#            filedata => {
#                setMode();
#                editor.setValue(filedata);
#                var fileType = currentFile.split("/")[0]; 
#                var fileName = currentFile.split("/")[1];
#                document.getElementById("newscrollinput").value = fileName;
#            }
#        );
#        
#        document.getElementById("currentfilename").innerHTML = currentFile;
#                
#    }
#}
#
#
#function setMode() {
#  // Extract everything after the last dot, converted to lowercase
#  const ext = currentFile.slice(currentFile.lastIndexOf('.')).toLowerCase();
#
#  // Define a map of extensions to Ace Editor modes
#  const modeMap = {
#    '.py': 'python',
#    '.txt': 'text',
#    '.md': 'markdown',
#    '.tex': 'latex',
#    '.js': 'javascript',
#    '.ino': 'java',
#    '.css': 'css',
#    '.php': 'php',
#    '.html': 'html',
#    '.json': 'json',
#    '.bat': 'batchfile',
#    '.sh': 'sh'
#  };
#
#  // Look up the mode, defaulting to 'text' if the extension isn't found
#  const mode = modeMap[ext] || 'text';
#  
#  editor.getSession().setMode(`ace/mode/${mode}`);
#}
#
#lightmode = false;
#
#document.getElementById("lightdarkbutton").onclick = function(){
#    lightmode = !lightmode;
#    if(lightmode){
#        document.getElementById("lightdarkbutton").style.color = "black";
#        document.getElementById("lightdarkbutton").style.borderColor = "black";
#        
#        document.getElementById("filescroll").style.backgroundColor = "white";
#
#        document.getElementById("filescroll").style.color = "black";        
#        document.getElementById("currentfilename").style.backgroundColor = "#eeeeee";
#        document.getElementById("currentfilename").style.color = "black";
#        document.getElementById("newscrollinput").style.color = "black";
#        document.getElementById("newscrollinput").style.backgroundColor = "white";
#        document.body.style.backgroundColor = "#b0b0b0";
#        document.body.style.color = "black";
#        document.getElementById("lightdarkbutton").innerHTML = "DARK MODE";
#        editor.setTheme("ace/theme/github");
#
#        var links = document.getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "blue";
#        }
#    }
#    else{
#        
#        document.getElementById("lightdarkbutton").style.color = "white";
#        document.getElementById("lightdarkbutton").style.borderColor = "white";
#        
#        document.body.style.backgroundColor = "#404040";
#        document.body.style.color = "white";
#
#        document.getElementById("filescroll").style.backgroundColor = "#101010";        
#        document.getElementById("filescroll").style.color = "white";        
#        
#        document.getElementById("currentfilename").style.backgroundColor = "#101010";        
#        document.getElementById("currentfilename").style.color = "white"
#        document.getElementById("newscrollinput").style.color = "white";
#        document.getElementById("newscrollinput").style.backgroundColor = "black";        
#        document.getElementById("lightdarkbutton").innerHTML = "LIGHT MODE";        
#        editor.setTheme("ace/theme/vibrant_ink");
#
#        var links = document.getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "#ff2cb4";
#        }        
#    }
#}
#</script>
#<style>
#a{
#    color:#ff2cb4;
#}
##inputtable{
#    position:absolute;
#    left:10px;
#    top:10px;
#    font-size:1.5em;
#    font-family:Arial;
#}
##newscrollinput{
#    font-family:courier;
#    
#}
##linktable{
#    position:absolute;
#    right:10px;
#    top:10px;
#    background-color:#808080;
#}
#body{
#    overflow:hidden;
#        font-family:Arial;
#
#}
#input{
#    font-family:Arial;
#    color:white;
#}
#
#.file{
#    cursor:pointer;
#    border-radius:0.25em;
#    border:solid;
#    padding:0.25em 0.25em 0.25em 0.25em;
#}
#.files:hover{
#    background-color:green;
#}
#.files:active{
#    background-color:yellow;
#}
##filescroll{
#    position:absolute;
#    overflow:scroll;
#    top:250px;
#    bottom:0%;
#    right:0%;
#    left:75%;
#    border:solid;
#    border-radius:5px;
#    border-width:3px;
#    font-family:Arial;
#    font-size:22px;
#    z-index:99999999;
#}
##maineditor{
#    position:absolute;  
#    left:0%;
#    top:150px;
#    bottom:1em;
#    right:30%;
#    font-size:22px;
#    border:solid;
#    border-color:black;
#}
#.button{
#    cursor:pointer;
#}
#.button:hover{
#    background-color:green;
#}
#.button:active{
#    background-color:yellow;
#}
##lightdarkbutton{
#    position:absolute;
#    right:0px;
#    top:0px;
#    right:5px;
#    top:5px;
#    text-align:center;
#    border:solid;
#    border-radius:3px;
#    font-size:2em;
#    border-color:white;
#    color:white;
#    font-family:Arial;
#}
#</style>
#
#</body>
#</html></dirt.html>
#<load-file.php>
#
#<?php
#$filename = $_REQUEST["filename"];//filename
#$data = file_get_contents($filename);//get contents of file
#echo $data;//print contents
#?></load-file.php>
#<save-file.php>
#
#<?php
#    $data = $_POST["data"]; //get data 
#    $filename = $_POST["filename"];//get filename
#    $file = fopen($filename,"w");// create new file with this name
#    fwrite($file,$data); //write data to file
#    fclose($file);  //close file
#?></save-file.php>
#<delete-file.php>
#
# <?php
#    $filename = $_POST["filename"];
#    unlink($filename);
#?></delete-file.php>
#<list-files.php>
#
#<?php
#
#    $directoryName = isset($_GET["directory"]) ? basename($_GET["directory"]) : '';
#    $targetPath = getcwd() . '/' . $directoryName;
#    $files = array_diff(scandir($targetPath), ['.', '..']);
#    echo json_encode(array_values($files));
#
#?>
#</list-files.php>
#<list-branches.php>
#
#<?php
#
#    $files = scandir(getcwd());
#    $dirs = array_filter($files, function ($value) {
#        return $value[0] !== '.' && is_dir($value);
#    });
#    echo json_encode(array_values($dirs));
#
#?>
#</list-branches.php>
#<delete-branch.php>
#
#<?php
#
#$branchname = $_POST["branch"];//get name of branch to kill
#
#rrmdir($branchname);//run recursive delet function
#
#function rrmdir($src) {
#    $dir = opendir($src);
#    while(false !== ( $file = readdir($dir)) ) {
#        if (( $file != '.' ) && ( $file != '..' )) {
#            $full = $src . '/' . $file;
#            if ( is_dir($full) ) {
#                rrmdir($full);
#            }
#            else {
#                unlink($full);//this is the delete command
#            }
#        }
#    }
#    closedir($dir);
#    rmdir($src);
#}
#
#
#?></delete-branch.php>
#<create-branch.php>
#
#<?php
#if(isset($_GET["branch"])){
#    $branch = $_GET["branch"];
#    mkdir($branch);
#
#    $targetPath = getcwd() . '/';
#    $files = array_diff(scandir($targetPath), ['.', '..']);
#    
#    $code_files = [];
#    $allowed_extensions = ['txt', 'html', 'css', 'js', 'json', 'php', 'md', 'sh', 'bat', 'ipynb', 'py'];
#    
#    foreach ($files as $file) {
#        $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
#        if (in_array($ext, $allowed_extensions)) {
#            $code_files[] = $file;
#        }
#    }
#    
#    foreach ($code_files as $file) {
#        @copy($file,$branch."/".$file);
#    }
#    
#}
#?>
#<a href = "<?php echo $branch?>/index.html"><?php echo $branch?>/index.html
#</a>
#<style>
#body{
#    font-size:3em;
#    font-family:arial;
#}
#a{
#    font-size:3em;
#    color:blue;
#}
#</style></create-branch.php>
#<php.js>
#
#
#function load_file(name) {
#    return fetch('load-file.php?filename=' + name).then(res => res.text());
#}
#
#
#function save_file(name,data){
#    fetch('save-file.php', {
#        method: 'POST',
#        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
#        body: 'data=' + data + '&filename=' + name
#    });
#}
#
#function delete_file(name){
#    fetch('delete-file.php', {
#        method: 'POST',
#        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
#        body: 'filename=' + name
#    });    
#}
#
#
#function delete_branch(name){
#    fetch('delete-branch.php', {
#        method: 'POST',
#        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
#        body: 'branch=' + name
#    });
#}
#
#function list_files(fork) {
#    var query = fork ? '?directory=' + encodeURIComponent(fork) : '';
#    return fetch('list-files.php' + query)
#        .then(res => res.json())
#        .then(files => {
#            return files; 
#        });
#}
#
#function list_branches(){
#    return fetch('list-branches.php')
#    .then(res => res.json())
#    .then(branches => {
#        return branches; 
#    });
#}
#
#</php.js>
#<php.html>
#
# <!doctype html>
#<html>
#<head>
# <!-- 
#edit files in .html, .js, .json, .css, .php, .py, .txt,  and .md
#-->
#
#    <link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/3gAA//8AAPb/AAD//wAA//8AAP/7AAD/3wAA3/8AAP7/AAD//wAA//8AAP93AADv/wAA//8AAP//AAB+/gAA" rel="icon" type="image/x-icon">
#    
#<!--
#ace.js project home:
#https://ace.c9.io/
#
#list of languages:
#https://cloud9-sdk.readme.io/docs/language-mode
#ace.js is BSD license
#
#-->    
#
#<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.43.3/ace.js"></script>
#
#<script src="php.js"></script>
#<title>php code editor</title>
#</head>
#<body>
#
#<div id = "lightdarkbutton" class = "button">LIGHT MODE</div>
#
#<a href=  "index.html" style = "position:absolute;right:5px;top:1.5em;font-size:2em;font-family:Arial">HOME</a>
#
#
#<table id = "inputtable">
#    <tr>
#        <td>Current File Name:</td>
#        <td id = "currentfilename"></td>
#    </tr>
#    <tr>
#        <td>New File Name(end with .html, .js, .css, .py, .bat, .json, .php, .md, .txt):</td>
#        <td><input id = "newscrollinput"/></td>
#    </tr>
#</table>
#
#<div id="maineditor" contenteditable="true" spellcheck="false"></div>
#
#
#<div id = "filescroll">
#
#</div>
#
#<script>
#
#
#editor = ace.edit("maineditor");
#editor.setTheme("ace/theme/github");
#//editor.setTheme("ace/theme/vibrant_ink");
#editor.getSession().setMode("ace/mode/html");
#editor.getSession().setUseWrapMode(true);
#editor.$blockScrolling = Infinity;
#editor.setTheme("ace/theme/vibrant_ink");
#editor.setOption("useWorker", false);
#
#currentFile = "php.html";
#
#
#load_file(currentFile).then(
#    filedata => {
#        setMode();
#        editor.setValue(filedata);
#        document.getElementById("currentfilename").innerHTML = currentFile;
#    }
#);
#
#
#scrolls = [];
#
#list_files().then(files => {
#    scrolls = files;
#    for(var index = 0;index < scrolls.length;index++) {    
#        if(scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".html" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".txt" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".css" || scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".php" || scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".js" ||scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".py" || scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".md" ||    scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".json"|| scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".bat"|| scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".sh"){
#     
#        if(scrolls[index].substring(scrolls[index].length-5,scrolls[index].length) == ".html"){
#            var newa = document.createElement("A");
#            newa.innerHTML = scrolls[index];
#            newa.href = scrolls[index];
#            document.getElementById("filescroll").appendChild(newa);
#         }             
#        var newscrollbutton = document.createElement("div");
#        newscrollbutton.classList.add("file");
#        newscrollbutton.classList.add("html");
#        if(scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".js"){
#            newscrollbutton.style.borderColor = "red";
#        }
#        if(scrolls[index].substring(scrolls[index].length-3,scrolls[index].length) == ".md"){
#            newscrollbutton.style.borderColor = "#0000ff80";
#        }
#        if(scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".css"){
#            newscrollbutton.style.borderColor = "yellow";
#        }
#        if(scrolls[index].substring(scrolls[index].length-4,scrolls[index].length) == ".php"){
#            newscrollbutton.style.borderColor = "purple";
#        }
#        newscrollbutton.innerHTML =  scrolls[index];
#        document.getElementById("filescroll").appendChild(newscrollbutton);
#        newscrollbutton.onclick = function(){
#            currentFile = this.innerHTML;
#            load_file(currentFile).then(
#                filedata => {
#                    setMode();
#                    editor.setValue(filedata);
#                    document.getElementById("currentfilename").innerHTML = currentFile;
#                    var fileType = currentFile.split("/")[0]; 
#                    var fileName = currentFile.split("/")[1];
#                    //document.getElementById("newscrollinput").value = fileName;
#                }
#            );
#
#        
#            document.getElementById("currentfilename").innerHTML = currentFile;
#            
#        }
#    
#        }
#    }
#
#});
#
#
#document.getElementById("currentfilename").innerHTML = currentFile;
#
#document.getElementById("maineditor").onkeyup = function(){
#    data = encodeURIComponent(editor.getSession().getValue());
#    save_file(currentFile,data);
#    var fileType = currentFile.split("/")[0]; 
#    var fileName = currentFile.split("/")[1];
#}
#
#document.body.style.backgroundColor = "#202020";
#document.body.style.color = "white";
#document.getElementById("newscrollinput").style.backgroundColor = "#202020";
#document.getElementById("newscrollinput").style.color = "white";        
#
#editor.setTheme("ace/theme/vibrant_ink");
#
#document.getElementById("newscrollinput").value = "";
#
#name = "";
#document.getElementById("newscrollinput").onchange = function(){
#    name = this.value;
#    currentFile = name;
#    scroll = editor.getSession().getValue();
#    setMode();
#    editor.setValue(scroll);  
#    data = encodeURIComponent(scroll);
#
#    save_file(currentFile,data);
#
#
#    addcodelink(name);
#    document.getElementById("currentfilename").innerHTML = currentFile;
#
#}
#
#
#function addcodelink(codename){
#    var newscrollbutton = document.createElement("div");
#    newscrollbutton.classList.add("file");
#    newscrollbutton.classList.add("html");
#    newscrollbutton.innerHTML = codename;
#    document.getElementById("filescroll").appendChild(newscrollbutton);
#    newscrollbutton.onclick = function(){
#        currentFile = this.innerHTML;
#        //use php script to load current file;
#
#
#        load_file(currentFile).then(
#            filedata => {
#                setMode();
#                editor.setValue(filedata);
#                var fileType = currentFile.split("/")[0]; 
#                var fileName = currentFile.split("/")[1];
#                document.getElementById("newscrollinput").value = fileName;
#            }
#        );
#        
#        document.getElementById("currentfilename").innerHTML = currentFile;
#                
#    }
#}
#
#
#function setMode() {
#  // Extract everything after the last dot, converted to lowercase
#  const ext = currentFile.slice(currentFile.lastIndexOf('.')).toLowerCase();
#
#  // Define a map of extensions to Ace Editor modes
#  const modeMap = {
#    '.py': 'python',
#    '.txt': 'text',
#    '.md': 'markdown',
#    '.tex': 'latex',
#    '.js': 'javascript',
#    '.ino': 'java',
#    '.css': 'css',
#    '.php': 'php',
#    '.html': 'html',
#    '.json': 'json',
#    '.bat': 'batchfile',
#    '.sh': 'sh'
#  };
#
#  // Look up the mode, defaulting to 'text' if the extension isn't found
#  const mode = modeMap[ext] || 'text';
#  
#  editor.getSession().setMode(`ace/mode/${mode}`);
#}
#
#lightmode = false;
#
#document.getElementById("lightdarkbutton").onclick = function(){
#    lightmode = !lightmode;
#    if(lightmode){
#        document.getElementById("lightdarkbutton").style.color = "black";
#        document.getElementById("lightdarkbutton").style.borderColor = "black";
#        
#        document.getElementById("filescroll").style.backgroundColor = "white";
#
#        document.getElementById("filescroll").style.color = "black";        
#        document.getElementById("currentfilename").style.backgroundColor = "#eeeeee";
#        document.getElementById("currentfilename").style.color = "black";
#        document.getElementById("newscrollinput").style.color = "black";
#        document.getElementById("newscrollinput").style.backgroundColor = "white";
#        document.body.style.backgroundColor = "#b0b0b0";
#        document.body.style.color = "black";
#        document.getElementById("lightdarkbutton").innerHTML = "DARK MODE";
#        editor.setTheme("ace/theme/github");
#
#        var links = document.getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "blue";
#        }
#    }
#    else{
#        
#        document.getElementById("lightdarkbutton").style.color = "white";
#        document.getElementById("lightdarkbutton").style.borderColor = "white";
#        
#        document.body.style.backgroundColor = "#404040";
#        document.body.style.color = "white";
#
#        document.getElementById("filescroll").style.backgroundColor = "#101010";        
#        document.getElementById("filescroll").style.color = "white";        
#        
#        document.getElementById("currentfilename").style.backgroundColor = "#101010";        
#        document.getElementById("currentfilename").style.color = "white"
#        document.getElementById("newscrollinput").style.color = "white";
#        document.getElementById("newscrollinput").style.backgroundColor = "black";        
#        document.getElementById("lightdarkbutton").innerHTML = "LIGHT MODE";        
#        editor.setTheme("ace/theme/vibrant_ink");
#
#        var links = document.getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "#ff2cb4";
#        }        
#    }
#}
#</script>
#<style>
#a{
#    color:#ff2cb4;
#}
##inputtable{
#    position:absolute;
#    left:10px;
#    top:10px;
#    font-size:1.5em;
#    font-family:Arial;
#}
##newscrollinput{
#    font-family:courier;
#    
#}
##linktable{
#    position:absolute;
#    right:10px;
#    top:10px;
#    background-color:#808080;
#}
#body{
#    overflow:hidden;
#}
#input{
#    font-family:Arial;
#    color:white;
#}
#
#.file{
#    cursor:pointer;
#    border-radius:0.25em;
#    border:solid;
#    padding:0.25em 0.25em 0.25em 0.25em;
#}
#.files:hover{
#    background-color:green;
#}
#.files:active{
#    background-color:yellow;
#}
##filescroll{
#    position:absolute;
#    overflow:scroll;
#    top:250px;
#    bottom:0%;
#    right:0%;
#    left:75%;
#    border:solid;
#    border-radius:5px;
#    border-width:3px;
#    font-family:Arial;
#    font-size:22px;
#    z-index:99999999;
#}
##maineditor{
#    position:absolute;  
#    left:0%;
#    top:150px;
#    bottom:1em;
#    right:30%;
#    font-size:22px;
#    border:solid;
#    border-color:black;
#}
#.button{
#    cursor:pointer;
#}
#.button:hover{
#    background-color:green;
#}
#.button:active{
#    background-color:yellow;
#}
##lightdarkbutton{
#    position:absolute;
#    right:0px;
#    top:0px;
#    right:5px;
#    top:5px;
#    text-align:center;
#    border:solid;
#    border-radius:3px;
#    font-size:2em;
#    border-color:white;
#    color:white;
#    font-family:Arial;
#}
#</style>
#
#</body>
#</html></php.html>
#<feed.html>
#
#<!doctype html>
#<html>
#<head>
#    <link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/3gAA//8AAPb/AAD//wAA//8AAP/7AAD/3wAA3/8AAP7/AAD//wAA//8AAP93AADv/wAA//8AAP//AAB+/gAA" rel="icon" type="image/x-icon">    
#    <script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.min.js"></script>
#    <script src = "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
#    <link rel="stylesheet" href="feed.css">
#    <title>FEED</title>
#</head>
#<body>
#    <div id ="qrcode"></div>
#    <input id = "post">
#    <div id ="feed"></div>
#    <div id = "clear">CLEAR</div>
#    <script src="feed.js"></script>
#</body>
#</html></feed.html>
#<feed.js>
#
#codesquaresize = 150;
#qrcode = new QRCode(document.getElementById("qrcode"), {
#	text: window.location.href,
#	width: codesquaresize,
#	height: codesquaresize,
#	colorDark : "#000000",
#	colorLight : "#ffffff",
#	correctLevel : QRCode.CorrectLevel.H
#});
#
#feed = [];
#
#document.getElementById("post").value = "";
#document.getElementById("post").select();
#
#document.getElementById("clear").onclick = function(){
#
#    feed = [];
#    loadFeed();
#    saveFeed();
#    document.getElementById("post").value = "";
#    document.getElementById("post").select();
#    
#}
#
#document.getElementById("post").onchange = function(){
#    if(this.value.slice(-5) == ".html" || this.value.slice(0,8) == "https://" || this.value.slice(0,8) == "HTTPS://" || this.value.slice(0,7) == "http://"){
#        post = "<a href = \"" + this.value + "\">" + this.value + "</a>";
#    }
#    else{
#        post = this.value;
#    }
#    feed.unshift(post);
#    this.value = "";
#    loadFeed();
#    saveFeed();
#}
#
#load_file('feed.json').then(
#    raw_feed => {
#        feed = JSON.parse(raw_feed);
#        loadFeed();
#    }
#);
#
#function loadFeed(){
#
#    document.getElementById("feed").innerHTML = "";
#    for(let index = 0;index < feed.length;index++){
#        let newSign = document.createElement("DIV");
#        newSign.id = "sign-" + index.toString();
#        newSign.className = "sign";
#        newSign.innerHTML = feed[index];
#        let deleteButton = document.createElement("SPAN");
#        deleteButton.className = "delete-button";
#        deleteButton.innerHTML = "DELETE";
#        deleteButton.onclick  = function(){
#            let localIndex = parseInt(this.parentNode.id.split("-")[1]);
#            let newFeed = [];
#            for(let index = 0;index < feed.length;index++){
#                if(index != localIndex){
#                    newFeed.push(feed[index]);
#                }
#            }
#            feed = newFeed;
#            saveFeed();
#            loadFeed();
#        }
#        newSign.appendChild(deleteButton);
#        document.getElementById("feed").appendChild(newSign);
#    }
#}
#
#function saveFeed(){
#    data = encodeURIComponent(JSON.stringify(feed,null,"   "));
#    save_file("feed.json",data);
#}
#
#function setup() {
#    frameRate(3);
#}
#
#function draw(){
#    //load feed
#    feedLength = feed.length;
#    load_file('feed.json').then(
#    raw_feed => {
#        feed = JSON.parse(raw_feed);
#        if(feedLength != feed.length){
#            loadFeed();
#        }
#    });
#}
#
#function load_file(name) {
#    return fetch('load-file.php?filename=' + name).then(res => res.text());
#}
#
#
#function save_file(name,data){
#    fetch('save-file.php', {
#        method: 'POST',
#        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
#        body: 'data=' + data + '&filename=' + name
#    });
#}
#
#</feed.js>
#<feed.css>
#
#body{
#    background-color:#979496;
#    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
#}
##qrcode img{
#    border:solid;
#    border-color:white;
#    border-width:25px;
#}
##post{
#    background-color:black;
#    color:#00ff00;
#    font-family:Courier;
#    font-size:3em;
#}
##clear:hover{
#    background-color:#400000;
#}
#
##clear{
#    font-size:3em;
#    color:red;
#    background-color:black;
#    width:6em;
#    border:solid;
#    border-radius:0.5em;
#    cursor:pointer;
#    border-color:red;
#    text-align:center;
#}
#.sign{
#  background-color: #9f8767;
#  font-size:2em;
#  font-family:Comic Sans MS;
#  border:solid;
#  padding:1em 1em 1em 1em;
#  margin:1em 1em 1em 1em;
#  border-radius:0.5em;
#}
#.delete-button{
#    color:red;
#    border:solid;
#    border-color:red;
#    background-color:black;
#    font-family:Arial;
#    padding:0.25em 0.25em 0.25em 0.25em;
#    border-radius:0.25em;
#    cursor:pointer;
#}
#.delete-button:hover{
#    background-color:#400000;
#}
#</feed.css>
#<feed.json>
#[
#   "SECOND POST",
#   "FIRST POST"
#]</feed.json>
#<wall.html>
#<!doctype html>
#<html lang="en">
#<head>
#    <meta charset="utf-8">
#
#    <!-- 
#
#        EVERYTHING IS PHYSICAL 
#        EVERYTHING IS FRACTAL
#        EVERYTHING IS RECURSIVE
#        NO MONEY 
#        NO MINING 
#        NO PROPERTY
#        LOOK AT THE INSECTS
#        LOOK AT THE FUNGI
#        LANGUAGE IS HOW THE MIND PARSES REALITY
#
#    -->
#    <title>FULL STACK TRASH MAGIC</title>
#<link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAZ4efAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEREREREREREREREREREREREAAAAAAAAREQEREREREBERAREREREQEREBEAAAARAREQEQEREBEBERARAQAQEQEREBEBABARAREQEQEREBEBERARAAAAEQEREBERERERAREQEREREREBERAAAAAAAAEREREREREREREREREREREREAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" rel="icon" type="image/x-icon">
#
#    <!--Stop Google:-->
#<META NAME="robots" CONTENT="noindex,nofollow">
#<script src = "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
#<script src = "php.js"></script>
#</head>
#<body>
#    <div id = "qrcode"></div>
#    <a style = "color:#ff2cb4; background-color:black; font-family:courier; position:absolute; left:25%; top:1em; z-index:666; font-size:3em;" href= "wall.txt">wall.txt</a>
#    
#    <h1 id = "title">wall.txt</h1>
#    <textarea id = "wall"></textarea>
#<script>
#
#codesquaresize = 150;
#qrcode = new QRCode(document.getElementById("qrcode"), {
#	text: window.location.href,
#	width: codesquaresize,
#	height: codesquaresize,
#	colorDark : "#000000",
#	colorLight : "#ffffff",
#	correctLevel : QRCode.CorrectLevel.H
#});
#
#wall = "";
#document.getElementById("wall").value = "";
#load_file("wall.txt").then(
#    filedata => {
#        wall = filedata.trim();
#        document.getElementById("wall").value = wall; 
#    }
#);
#
#
#document.getElementById("wall").onkeyup = function() {
#    wall = this.value;
#    data = encodeURIComponent(this.value);
#    save_file("wall.txt",wall);
#}
#
#
#</script>
#<style>
##title {
#  position: absolute;
#  top: 10px;
#  right: 10px;
#  font-size: clamp(1.5em, 5vw, 3em);
#}
#
##qrcode {
#  position: absolute;
#  top: 10px;
#  left: 10px;
#}
#
##wall {
#  font-family: Comic Sans MS;
#  background-color: #9f8767;
#  box-sizing: border-box;
#  border-radius: 0.5em;
#  padding: 0.5em;
#  position: absolute;
#  top: max(180px, 25vw);
#  left: 10px;
#  bottom: 10px;
#  right: 10px;
#  font-size: clamp(1.2em, 4vw, 3em);
#}
#
#body {
#  background-color: #9f8767;
#  font-family:  Comic Sans MS;
#}
#
#@media (min-width: 768px) {
#  #wall {
#    top: 180px;
#    font-size: 3em;
#  }
#}
#
#
#
#</style>
#</body>
#</html></wall.html>
#<wall.txt>
#WE ARE ALL JUST BRICKS IN THE WALL</wall.txt>
#<README.md>
## dirt
#
#```
#curl -o dirtspore.py [url]/dirtspore.py
#python dirtspore.py
#python dirt.py
#```
#
### [dirtspore.py](dirtspore.py)</README.md>
#<readme.html>
# <!doctype html>
#<html>
#<head>
#<!--Stop Google:-->
#<META NAME="robots" CONTENT="noindex,nofollow">
#    
#<link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAADw8OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAABAAEAAAAQAAEAERAAABARAQEREQAAEBEBAAEAAAAREREAAQAAABEAEQABAAAAEQARAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//wAA//8AAP//AAD//wAA3u8AAN7HAADSgwAA0u8AAMDvAADM7wAAzO8AAP//AAD//wAA//8AAP//AAD//wAA" rel="icon" type="image/x-icon">
#
#    
#<!--
#ace.js project home:
#https://ace.c9.io/
#
#list of languages:
#https://cloud9-sdk.readme.io/docs/language-mode
#
#
#-->    
#
#<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.6/ace.js" type="text/javascript" charset="utf-8"></script>
#    <script src = "https://cdnjs.cloudflare.com/ajax/libs/showdown/1.8.6/showdown.js"></script>
#
#        <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
#        <script>
#            MathJax.Hub.Config({
#                tex2jax: {
#                inlineMath: [['$','$'], ['\\(','\\)']],
#                processEscapes: true,
#                processClass: "mathjax",
#                ignoreClass: "no-mathjax"
#                }
#            });//			MathJax.Hub.Typeset();//tell Mathjax to update the math
#        </script>
#        <script src ="php.js"></script>
#<title>README.md EDITOR</title>
#</head>
#<body>
#<h1>README.md</h1>
#<div id = "lightdarkbutton" class = "button">--> DARK MODE <--</div>
#<div class = "no-mathjax" id = "maineditor" contenteditable="true" spellcheck="false"></div>
#<div class = "mathjax" id = "displayscroll"></div>
#
#<script>
#
#editor = ace.edit("maineditor");
#editor.setTheme("ace/theme/github");
#//editor.setTheme("ace/theme/vibrant_ink");
#//editor.getSession().setMode("ace/mode/html");
#editor.getSession().setMode("ace/mode/markdown");
#
#editor.getSession().setUseWrapMode(true);
#editor.$blockScrolling = Infinity;
#
#var converter = new showdown.Converter();
#// for more on options see here:
#// https://github.com/showdownjs/showdown/wiki/Showdown-Options
#converter.setOption('literalMidWordUnderscores', 'true');
#converter.setOption('tables', 'true')
#    
#currentFile = "README.md";
#
#load_file(currentFile).then(
#    readme => {
#        rawhtml = converter.makeHtml(readme);
#        document.getElementById("displayscroll").innerHTML = rawhtml;
#        MathJax.Hub.Typeset();//tell Mathjax to update the math
#        editor.setValue(readme.trim());
#    }
#);
#
#
#
#document.getElementById("maineditor").onkeyup = function(){
#    data = encodeURIComponent(editor.getSession().getValue());
#    save_file(currentFile,data);
#}
#
#
#lightmode = true;
#document.getElementById("lightdarkbutton").style.color = "black";
#document.getElementById("lightdarkbutton").style.borderColor = "black";
#
#document.getElementById("displayscroll").style.backgroundColor = "white";
#document.getElementById("displayscroll").style.color = "black";        
#document.getElementById("lightdarkbutton").innerHTML = "DARK MODE";
#editor.setTheme("ace/theme/github");
#var links = document.getElementById("displayscroll").getElementsByTagName("a");
#for(var index = 0;index < links.length;index++){
#    links[index].style.color = "blue";
#}
#
#document.getElementById("lightdarkbutton").onclick = function(){
#    lightmode = !lightmode;
#    if(lightmode){
#        document.getElementById("lightdarkbutton").style.color = "black";
#        document.getElementById("lightdarkbutton").style.borderColor = "black";
#        document.getElementById("lightdarkbutton").style.backgroundColor = "white";
#        document.getElementById("displayscroll").style.backgroundColor = "white";
#        document.getElementById("displayscroll").style.color = "black";        
#        document.getElementById("lightdarkbutton").innerHTML = "DARK MODE";
#        editor.setTheme("ace/theme/github");
#        var links = document.getElementById("displayscroll").getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "blue";
#        }
#    }
#    else{
#        
#        document.getElementById("lightdarkbutton").style.color = "white";
#        document.getElementById("lightdarkbutton").style.borderColor = "white";
#        document.getElementById("lightdarkbutton").style.backgroundColor = "#101010";
#        document.getElementById("displayscroll").style.backgroundColor = "#101010";        
#        document.getElementById("displayscroll").style.color = "white";        
#        document.getElementById("lightdarkbutton").innerHTML = "LIGHT MODE";        
#        editor.setTheme("ace/theme/vibrant_ink");
#
#        var links = document.getElementById("displayscroll").getElementsByTagName("a");
#        for(var index = 0;index < links.length;index++){
#            links[index].style.color = "#ff2cb4";
#        }        
#    }
#}
#
#</script>
#<style>
#body{
#    overflow:hidden;
#    font-family:Arial;
#    background-color:#808080;
#}
#a{
#    color:blue;
#}
#input{
#    font-family:courier;
#    color:white;
#}
#h1{
#    text-align:center;
#}
##maineditor{
#    position:absolute;  
#    left:1em;
#    top:5em;
#    right:50%;
#    bottom:1em;
#    font-size:1em;
#    border:solid;
#}
##displayscroll{
#    position:absolute;
#    left:55%;
#    right:1em;
#    bottom:1em;
#    top:5em;
#    border:solid;
#    border-width:3px;
#    overflow:scroll;
#    padding: 1em 1em 1em 1em;
#    background-color:white;
#}
##displayscroll img{
#    max-width:70%;
#    display:block;
#    margin:auto;
#}
#.button{
#    cursor:pointer;
#    background-color:white;
#    
#}
#.button:hover{
#    background-color:green;
#}
#.button:active{
#    background-color:yellow;
#}
##lightdarkbutton{
#    position:absolute;
#    right:10px;
#    top:10px;
#    width:10em;
#    text-align:center;
#    border:solid;
#    border-radius:3px;
#    font-size:2em;
#    color:black;
#}
#
#</style>
#
#</body>
#</html></readme.html>
#
