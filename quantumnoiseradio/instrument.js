const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');
}

knobIndex = -1;

function setup() {
     
    let container = document.getElementById('p5-canvas-container');
    let canvas = createCanvas(innerWidth - 30, innerHeight - 30);
    canvas.parent('p5-canvas-container');
    unit = width/2;

}

function draw() {
    clear();
    line(width/2,0,width/2,height);
    stroke(0);
    circle(mouseX,mouseY,10);
    line(0,unit,width,unit);
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
