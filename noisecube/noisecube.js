const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');//this talks to instrument.py, while port 8086 talks to dirt.py
}

controlIndex = 0;

noisecube = {};
noisecube.values = {
    "qubit_flux_bias":{
        "dc_offset":0,
        "ac_vpp":0,
        "ac_frequency":220
    },
    "noise_source_bias":{
        "dc_offset":0,
        "ac_vpp":0,
        "ac_frequency":440
    },
    "radio_pump":{
        "power":-30,
        "frequency":6e9
    },
    "radio_probe":{
        "power":-70,
        "frequency":5e9
    },
    "radio_spectrum":{
        "center_frequency":5.5e9,
        "frequency_sweep_width":0.2e9
    },
    "audio_spectrum":{
        "on":true
    }
};

noisecube.controls = [{
    "knob_mode":"qubit_flux_bias",
    "knobs":[[0,0,0],[0,0,0],[0,0,0]],
    "quantities":["dc_offset","ac_vpp","ac_frequency"],
    "units":["V","V","Hz"],
    "multipliers":[[0.1,0.01,0.001],[0.1,0.01,0.001],[100,10,1]],
    "max":[1,1,5000],
    "min":[-1,-1,100],
    "defaults":[0,0,440],
    "values":[0,0,440]
}];

noisecube.controls[0].values[0] = noisecube.controls[0].defaults[0]
noisecube.controls[0].values[0] += noisecube.controls[0].multipliers[0][0]*noisecube.controls[0].knobs[0][0];
noisecube.controls[0].values[0] += noisecube.controls[0].multipliers[0][1]*noisecube.controls[0].knobs[0][1];
noisecube.controls[0].values[0] += noisecube.controls[0].multipliers[0][2]*noisecube.controls[0].knobs[0][2];


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
    stroke(0);
    strokeWeight(1);
    line(width/2,0,width/2,height);
    knobIndex = -1;//always -1 when mouse not in knob
    strokeWeight(1);
    fill(0);
    textSize(20);
    text(noisecube.controls[controlIndex].knob_mode,5,25);
    
    

    
    
    for(row = 0; row < 3; row++){
        noisecube.controls[0].values[row] = noisecube.controls[0].defaults[row]
        noisecube.controls[0].values[row] += noisecube.controls[0].multipliers[row][0]*noisecube.controls[0].knobs[row][0];
        noisecube.controls[0].values[row] += noisecube.controls[0].multipliers[row][1]*noisecube.controls[0].knobs[row][1];
        noisecube.controls[0].values[row] += noisecube.controls[0].multipliers[row][2]*noisecube.controls[0].knobs[row][2];
        noisecube.controls[0].values[row] = Math.round(noisecube.controls[0].values[row]*1000)/1000;
        
        if(noisecube.controls[0].values[row] > noisecube.controls[0].max[row]){
            noisecube.controls[0].values[row] = noisecube.controls[0].max[row];
        }
        if(noisecube.controls[0].values[row] < noisecube.controls[0].min[row]){
            noisecube.controls[0].values[row] = noisecube.controls[0].min[row];
        }        
        strokeWeight(1);
        fill(0);
        text(noisecube.controls[controlIndex].quantities[row] + " = " + noisecube.controls[0].values[row] + " " + noisecube.controls[controlIndex].units[row],5,knob_origin_y + knob_spacing_y*row - 10 - knob_radius);
        
        for(col = 0; col < 3; col++){
            knob_x = knob_origin_x + col*knob_spacing_x;
            knob_y = knob_origin_y + row*knob_spacing_y;
            strokeWeight(1);
            fill(0);
            text(noisecube.controls[0].knobs[row][col]+"x"+noisecube.controls[0].multipliers[row][col],knob_x - 10,knob_y + knob_radius + 25);
            strokeWeight(5);
            fill(255);
    
            knob_distance = Math.sqrt( (knob_x - mouseX)**2  + (knob_y - mouseY)**2);
            if(knob_distance < knob_radius){
                fill("#00ff0080");
                knobIndex = 3*row + col;
            }
            else{
                fill(255);
            }
            circle(knob_x,knob_y,knob_diameter);
            line(knob_x,knob_y,knob_x + knob_radius*Math.sin(2*Math.PI*noisecube.controls[controlIndex].knobs[row][col]/knobClicks), knob_y - knob_radius*Math.cos(2*Math.PI*noisecube.controls[controlIndex].knobs[row][col]/knobClicks));
            
//            line(knobs[rowIndex][columnIndex].x,knobs[rowIndex][columnIndex].y,knobs[rowIndex][columnIndex].x + knob_radius*Math.sin(2*Math.PI*qnr.knobs[rowIndex][columnIndex]/knobClicks),knobs[rowIndex][columnIndex].y - knob_radius*Math.cos(2*Math.PI*qnr.knobs[rowIndex][columnIndex]/knobClicks));

//

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
