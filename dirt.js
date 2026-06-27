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

let isFetching = false;  

// Setup the connection
const socket = new WebSocket("ws://127.0.0.1:8080");
let serverReady = true;

// FIX 1: Set up the invisible double-buffer images automatically on startup
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
    // Extract the raw base64 URL inside the <img> tag sent from Python
    const parser = new DOMParser();
    const doc = parser.parseFromString(event.data, 'text/html');
    const imgTag = doc.querySelector('img');
    
    if (imgTag) {
        const newSrc = imgTag.getAttribute('src');
        
        // Determine which image element is currently hidden in the background
        const nextImgIndex = currentImgIndex === 1 ? 2 : 1;
        const activeImg = document.getElementById(`py-img-${currentImgIndex}`);
        const nextImg = document.getElementById(`py-img-${nextImgIndex}`);
        
        if (nextImg && activeImg) {
            // Load the new image completely in the background
            nextImg.src = newSrc;
            
            // FIX 2: Only swap visibility AFTER the browser has completely processed the new image
            nextImg.onload = function() {
                nextImg.style.opacity = "1";   // Fade the new image in instantly
                activeImg.style.opacity = "0";  // Hide the old image seamlessly
                currentImgIndex = nextImgIndex; // Swap roles for the next frame
                
                // Open the gate for the next p5.js frame calculation
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
  // Code to run.
  p5jsData.mouse.left_click = !p5jsData.mouse.left_click;
}
