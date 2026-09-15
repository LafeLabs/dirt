const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');//this talks to instrument.py, while port 8086 talks to dirt.py
}

controlIndex = 0;

noisecube = {};

noisecube.controls = [{
    "knob_mode":"qubit_flux_bias",
    "knobs":[[0,0,0],[0,0,0],[0,0,0]],
    "quantities":["dc_offset","ac_vpp","ac_frequency"],
    "units":["V","V","Hz"],
    "multipliers":[[0.1,0.01,0.001],[0.1,0.01,0.001],[100,10,1]],
    "maxima":[1,1,5000],
    "minima":[-1,-1,100],
    "defaults":[0,0,220]
}];


knobIndex = -1;//always -1 when mouse not in knob
buttonIndex = -1;//always -1 when mouse not in button

knobClicks = 24;

canvas_width = innerWidth - 30;
canvas_height = innerHeight - 30;

square_width = canvas_width/2;
knob_diameter = 0.5*square_width/3;
knob_radius = knob_diameter/2;
knob_origin_x = square_width/6;
knob_origin_y = square_width/6;
knob_spacing_x = square_width/3;
knob_spacing_y = square_width/3;

footer_height = innerHeight - square_width;

button_width = 0.94*square_width/3;
button_height = 0.8*footer_height/3;
button_origin_x =  square_width/6;
button_origin_y =  square_width + footer_height/3;
button_spacing_x = square_width/3;
button_spacing_y = footer_height/3;



function setup() {

    let container = document.getElementById('p5-canvas-container');
    let canvas = createCanvas(canvas_width,canvas_height);
    canvas.parent('p5-canvas-container');
    
}

function draw() {

    clear();
    fill(255);
    stroke(0);
    strokeWeight(1);
    line(width/2,0,width/2,height);
    strokeWeight(5);
    knobIndex = -1;//always -1 when mouse not in knob
    for(row = 0; row < 3; row++){
        for(col = 0; col < 3; col++){

            knob_x = knob_origin_x + col*knob_spacing_x;
            knob_y = knob_origin_y + row*knob_spacing_y;
            knob_distance = Math.sqrt( (knob_x - mouseX)**2  + (knob_y - mouseY)**2);
            if(knob_distance < knob_radius){
                fill("#00ff0080");
                knobIndex = 3*row + col;
            }
            else{
                fill(255);
            }
            circle(knob_x,knob_y,knob_diameter);
            line(knob_x,knob_y,knob_x + );

//noisecube.controls[controlIndex].knobs[Math.floor(knobIndex/3)][knobIndex%3]

        }
    }

    strokeWeight(5);
    buttonIndex = -1;//always -1 when mouse not in button
    fill(255);
    for(row = 0; row < 2; row++){
        for(col = 0; col < 3; col++){
            button_x = button_origin_x + col*button_spacing_x;
            button_y = button_origin_y + row*button_spacing_y;
            if(Math.abs(mouseX - button_x) < 0.5*button_width && Math.abs(mouseY - button_y) < 0.5*button_height){
                fill("#00ff0080");
                buttonIndex = 3*row + col;
            }
            else{
                fill(255);
            }
            rect(button_x - 0.5*button_width,button_y - 0.5*button_height,button_width,button_height);
            
        }
    }
    
}

function mouseWheel(event) {
    if(knobIndex >= 0){
        if(event.delta < 0){ 
            noisecube.controls[controlIndex].knobs[Math.floor(knobIndex/3)][knobIndex%3]++;
            
        }
        else{
            noisecube.controls[controlIndex].knobs[Math.floor(knobIndex/3)][knobIndex%3]--;
        }

    }
}

function sendData(instrumentData) {
  if (!debug_mode && socket) {
    socket.send(JSON.stringify(instrumentData));
  } else {
    console.log("Debug Mode (No Socket Connection):", instrumentData);
  }
}

function mouseClicked() {
  
//    alert(buttonIndex);
}
