const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');
}

knobIndex = -1;


load_file("instrument.json").then(
    filedata => {
        qnr = JSON.parse(filedata);
    }
);


function setup() {
     
    let container = document.getElementById('p5-canvas-container');
    let canvas = createCanvas(innerWidth - 30, innerHeight - 30);
    canvas.parent('p5-canvas-container');
    unit = width/2;
    knob_size = unit/3 - 80;
    bottom_height = height - unit;    
    button_width = unit/3 - 20;
    button_height = bottom_height/3 - 10;
}

function draw() {
    clear();
    line(width/2,0,width/2,height);
    stroke(0);
    
//    line(mouseX,0,mouseX,height);    
  //  line(0,mouseY,width,mouseY);
    line(0,unit,width,unit);
    rect(10,height - bottom_height/3 + 5,button_width,button_height);
    rect(10,height - 2*bottom_height/3 + 5,button_width,button_height);
    rect(10,height - 3*bottom_height/3 + 5,button_width,button_height);

    rect(unit/3 + 10,height - bottom_height/3 + 5,button_width,button_height);
    rect(unit/3 + 10,height - 2*bottom_height/3 + 5,button_width,button_height);
    rect(unit/3 + 10,height - 3*bottom_height/3 + 5,button_width,button_height);

    rect(2*unit/3 + 10,height - bottom_height/3 + 5,button_width,button_height);
    rect(2*unit/3 + 10,height - 2*bottom_height/3 + 5,button_width,button_height);
    rect(2*unit/3+10,height - 3*bottom_height/3 + 5,button_width,button_height);
    
    circle(unit/6,unit/6,knob_size);
    circle(unit/2,unit/6,knob_size);
    circle(5*unit/6,unit/6,knob_size);
    circle(unit/6,unit/2,knob_size);
    circle(unit/2,unit/2,knob_size);
    circle(5*unit/6,unit/2,knob_size);
    circle(unit/6,5*unit/6,knob_size);
    circle(unit/2,5*unit/6,knob_size);
    circle(5*unit/6,5*unit/6,knob_size);

}

function mouseWheel(event) {
    if(knobIndex >= 0){
        if(event.delta < 0){ 

        }
        else{

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
