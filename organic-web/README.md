# dirt

## human body &harr; p5js &harr; python

## self-replicating code swarm

## [replicator spore dirt.php](https://github.com/LafeLabs/dirt/blob/main/dirt.php)

## dirt.html

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQAAfX0AAH19AAB9fQAAfX0AAH19AAB9fQAAfX0AAH19AAB9fQAAfX0AAH19AAB9fQAAfX0AAH19AAABAQAA" rel="icon" type="image/x-icon">
   <title>dirt</title>
   <script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.js"></script>
   <script src = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/addons/p5.sound.js"></script>
    <link rel="stylesheet" href="dirt.css">
    <script src="dirt.js"></script>    
</head>
<body> 
    <main></main>
    <div id = "live-html"></div>
</div>
</body>
</html>
```

## dirt.css

```css
main{
    position:absolute;
    left:1%;
    top:1%;
    border:solid;
    border-radius:0.3%;
    border-width:0.3%;
}
#live-html{
    position:absolute;
    right:1%;
    top:1%;
    bottom:1%;
    width:48%;
    border:solid;
    border-radius:0.3%;
    border-width:0.3%;
}

```

## dirt.js

```javascript
p5jsData = {
    "glyph":[],
    "audio_spectrum":[],
    "spectrum_bin_frequency":21.533,
    "keystroke":"",
    "mouse":{
        "x":0,
        "y":0,
        "wheel":0,
        "left_click":false
    }
};

var mic, fft;

brushstroke = [];
thispoint = {};
thispoint.x = 0;
thispoint.y = 0;

const socket = new WebSocket("ws://127.0.0.1:8080");
let serverReady = true;
let currentImgIndex = 1;
window.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("live-html");
    if (container) {
        container.innerHTML = `
            <div style="position: relative; width: 100%; height: auto;">
                <img id="py-img-1" style="position: absolute; top: 0; left: 0; width: 100%; height: auto; display: block; opacity: 1;">
                <img id="py-img-2" style="position: absolute; top: 0; left: 0; width: 100%; height: auto; display: block; opacity: 0;">
            </div>
        `;
    }
});

socket.onmessage = function(event) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(event.data, 'text/html');
    const imgTag = doc.querySelector('img');
    
    if (imgTag) {
        const newSrc = imgTag.getAttribute('src');
        const nextImgIndex = currentImgIndex === 1 ? 2 : 1;
        const activeImg = document.getElementById(`py-img-${currentImgIndex}`);
        const nextImg = document.getElementById(`py-img-${nextImgIndex}`);
        
        if (nextImg && activeImg) {
            nextImg.src = newSrc;
            nextImg.onload = function() {
                nextImg.style.opacity = "1";
                activeImg.style.opacity = "0";
                currentImgIndex = nextImgIndex;
                serverReady = true; 
            };
        } else {
            serverReady = true;
        }
    } else {
        serverReady = true;
    }
};

function setup() {
    control_canvas_width = 0.48*innerWidth;
    createCanvas(0.48*innerWidth,0.97*innerHeight);  
    mic = new p5.AudioIn();
    mic.start();
    fft = new p5.FFT();
    fft.setInput(mic);
    frameRate(20); 
    stroke(0);
    strokeWeight(20);
}

inLine = false;
function draw(){
    p5jsData.audio_spectrum = fft.analyze();
    nyquistFreq = sampleRate() / 2;
    p5jsData.spectrum_bin_frequency = nyquistFreq / (p5jsData.audio_spectrum.length);
    fill(255);
    noStroke();     
    rect(0, height - 100, width, height); 
    stroke(0);
    strokeWeight(1);
    noFill();
    beginShape();
    vertex(0,height);
    for (let index = 0; index < p5jsData.audio_spectrum.length; index++) {
        vertex(index, map(p5jsData.audio_spectrum[index], 0, 255, height, height - 100));
    }
    vertex(width,height);
    endShape(); 
    stroke(0);
    strokeWeight(30);
    
    if(mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height){
        p5jsData.mouse.x = mouseX;
        p5jsData.mouse.y = mouseY;
    }
    
    if(mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < width){
      if (mouseIsPressed === true) {
        if(inLine == false){
            var point = {};
            point.x = Math.round(1024*mouseX/width);
            point.y = Math.round(1024*mouseY/width);
            brushstroke.push(point);
        }
        line(mouseX, mouseY, pmouseX, pmouseY);
        inLine = true;
        if(mouseX != pmouseX || mouseY != pmouseY){
            var point = {};
            point.x = Math.round(1024*mouseX/width);
            point.y = Math.round(1024*mouseY/width);
            brushstroke.push(point);
        }
      }
      else{
          if(inLine){
              p5jsData.glyph.push(JSON.parse(JSON.stringify(brushstroke)));
              brushstroke = [];
          }
          inLine = false;
      }
    }
    
    if (socket.readyState === WebSocket.OPEN && serverReady === true) {
        serverReady = false; 
        socket.send(JSON.stringify(p5jsData));
    }
    
}

function mouseWheel(event) {
    if(mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height){
        if(event.delta > 0){ 
            p5jsData.mouse.wheel--;
        }
        else{
            p5jsData.mouse.wheel++;
        }
    }
}

function keyPressed() {
    if(mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height){
        p5jsData.keystroke = key;
    }
}

function mouseClicked() {
  p5jsData.mouse.left_click = !p5jsData.mouse.left_click;
}

```

## dirt.py

```python
import asyncio
import json
import websockets
import io
import base64

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

async def handle_connection(websocket):
    print("[CONNECTED] Python is standing by for p5.js requests.")
    try:
        while True:
            p5js_data_raw = await websocket.recv()
            p5js_data = json.loads(p5js_data_raw)
            plt.figure(1, figsize=(6, 6))
            plt.clf()
            for stroke in p5js_data.get('glyph', []):
                if not stroke:
                    continue
                xdata = [point['x'] for point in stroke]
                ydata = [point['y'] for point in stroke]
                
                xdata += 8 * np.random.randn(len(xdata))
                ydata += 8 * np.random.randn(len(ydata))
                
                plt.plot(xdata, ydata, color='black', linewidth=10, solid_capstyle='round')
            plt.xlim(0, 1023)
            plt.ylim(0, 1023)
            p5js_data["mouse"]["x"] = np.round(p5js_data["mouse"]["x"])
            p5js_data["mouse"]["y"] = np.round(p5js_data["mouse"]["y"])

            plt.text(10,50,f'key = {p5js_data["keystroke"]}')
            plt.text(10,100,f'mouse x = {p5js_data["mouse"]["x"]}')
            plt.text(10,150,f'mouse y = {p5js_data["mouse"]["y"]}')
            plt.text(10,200,f'mouse wheel = {p5js_data["mouse"]["wheel"]}')
            peak_audio_frequency = np.argmax(p5js_data["audio_spectrum"])*p5js_data["spectrum_bin_frequency"]
            plt.text(10,250,f'peak frequency = {peak_audio_frequency} Hz')
            plt.gca().invert_yaxis() 
            plt.axis('off')          
            plt.tight_layout(pad=0)
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight', pad_inches=0)
            img_buf.seek(0)
            
            b64_string = base64.b64encode(img_buf.read()).decode('utf-8')
            imagedata = f"data:image/png;base64,{b64_string}"
            html_response = f'<img src="{imagedata}" style="width:100%; height:auto;">'
            await websocket.send(html_response)
    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] p5.js stopped the stream.")

async def main():
    async with websockets.serve(handle_connection, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

```

## dirt.bat

```batch
@echo off
echo Switching folders...
cd /d "C:\xampp\htdocs\dirt"
echo Launching Python...
call "%USERPROFILE%\anaconda3\Scripts\activate.bat" "%USERPROFILE%\anaconda3"
echo running python
python dirt.py
pause

```

## dirt.php

```php
<?php
$spore = "https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.php";
$baseurl = explode("dirt.php",$spore)[0];

@copy($baseurl."index.html","index.html");
@copy($baseurl."README.md","README.md");
@copy($baseurl."edit-files.html","edit-files.html");
@copy($baseurl."save-file.php","save-file.php");
@copy($baseurl."save-file-get.php","save-file-get.php");
@copy($baseurl."load-file.php","load-file.php");
@copy($baseurl."list-files.html","list-files.php");

$fileExtensions = ["html", "css", "js", "py", "bat", "md", "php", "json"];
foreach ($fileExtensions as $extension) {
    @copy($baseurl."dirt.".$extension,"dirt.".$extension);
}
if (!is_dir("data")) {
    mkdir("data");
}
if (!is_dir("plots")) {
    mkdir("plots");
}
?>
<a href = "index.html">index.html</a>
<style>
body{
    font-size:3em;
    font-family:arial;
}
a{
    font-size:3em;
    color:blue;
}
</style>
```

## dirt.json

```json
{
    "spore":"https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.php"
}
```


## [dirt.md](dirt.md)