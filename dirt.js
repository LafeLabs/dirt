
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
thispoint.x = 0;//x position in units of 1/1024 of width
thispoint.y = 0;//y position in units of 1/1024 of height from top

let isFetching = false;  //  guard flag defined in the fetch function

const socket = new WebSocket("ws://127.0.0.1:8080");

socket.onmessage = function(event) {
    // Dynamically update the viewport when Python answers back
    document.getElementById("live-html").innerHTML = event.data;
};


function setup() {
    control_canvas_width = 0.48*innerWidth;
    createCanvas(0.48*innerWidth,0.97*innerHeight);  
    mic = new p5.AudioIn();
    mic.start();
    fft = new p5.FFT();
    fft.setInput(mic);

    stroke(0);
    strokeWeight(20);

}


inLine = false;
function draw(){

    //listen to the microphone and turn it into data, plot the data
    p5jsData.audio_spectrum = fft.analyze();
    nyquistFreq = sampleRate() / 2;
    binFreq = nyquistFreq / (p5jsData.audio_spectrum.length);
    fill(255);
    noStroke();     
    rect(0, height - 100, width, height); // Draws across the bottom 100px
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
    

    // get mouse position if it is in the p5js canvas:    
    if(mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height){
        p5jsData.mouse.x = mouseX;
        p5jsData.mouse.y = mouseY;
    }
    // if it is in the upper square, add any brush strokes to the glyph:
    if(mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < width){
      if (mouseIsPressed === true) {
        if(inLine == false){
            var  point = {};
            point.x = Math.round(1024*mouseX/width);
            point.y = Math.round(1024*mouseY/width);
            brushstroke.push(point);
        }
        line(mouseX, mouseY, pmouseX, pmouseY);
        inLine = true;
        if(mouseX != pmouseX || mouseY != pmouseY){
            var  point = {};
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
    
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(p5jsData));
    } else {
        // Optional: Diagnostic log to track status if things stall
        console.log("WebSocket is initializing... current state: " + socket.readyState);
    }
    
    p5jsData.keystroke = "";
    p5jsData.left_click = false;
    
}

// if mouse wheel event, update the mouse wheel data
function mouseWheel(event) {
    if(mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height){
        if(event.delta > 0){ //mouse wheel down
            p5jsData.mouse.wheel--;
        }
        else{
            p5jsData.mouse.wheel++;
        }
    }
}


// if a key is pressed, update the key variable
function keyPressed() {
    if(mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height){
        p5jsData.keystroke = key;
    }
}

