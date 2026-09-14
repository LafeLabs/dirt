const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');
}

knobIndex = -1;//always -1 when mouse not in knob
buttonIndex = -1;//always -1 when mouse not in button

let qnr = {};
let isLoaded = false;


function preload() {

    load_file("instrument.json").then(
        filedata => {
            qnr = JSON.parse(filedata);
        }
    );

}

function setup() {

    load_file("instrument.json").then(filedata => {
        qnr = JSON.parse(filedata);
        isLoaded = true;
    });
    
    let container = document.getElementById('p5-canvas-container');
    let canvas = createCanvas(innerWidth - 30, innerHeight - 30);
    canvas.parent('p5-canvas-container');
    unit = width/2;
    knob_size = unit/3 - 80;
    knob_radius = knob_size/2;
    bottom_height = height - unit;    
    button_width = unit/3 - 20;
    button_height = bottom_height/3 - 10;

    knobs = [
        [
            {
                "x":unit/6,
                "y":unit/6
            },
            {
                "x":unit/2,
                "y":unit/6
            },
            {
                "x":5*unit/6,
                "y":unit/6
            }
        ],
        [
            {
                "x":unit/6,
                "y":unit/2
            },
            {
                "x":unit/2,
                "y":unit/2
            },
            {
                "x":5*unit/6,
                "y":unit/2
            }
        ],
        [
            {
                "x":unit/6,
                "y":5*unit/6
            },
            {
                "x":unit/2,
                "y":5*unit/6
            },
            {
                "x":5*unit/6,
                "y":5*unit/6
            }
        ]
    ];

    buttons = [
    [
        {
            "x":10,
            "y":height - 3*bottom_height/3 + 5
        },
        {
            "x":unit/3 + 10,
            "y":height - 3*bottom_height/3 + 5
        },
        {
            "x":2*unit/3 + 10,
            "y":height - 3*bottom_height/3 + 5
        }
    ],
    [
        {
            "x":10,
            "y":height - 2*bottom_height/3 + 5
        },
        {
            "x":unit/3 + 10,
            "y":height - 2*bottom_height/3 + 5
        },
        {
            "x":2*unit/3 + 10,
            "y":height - 2*bottom_height/3 + 5
        }
    ],
    [
        {
            "x":10,
            "y":height - 1*bottom_height/3 + 5
        },
        {
            "x":unit/3 + 10,
            "y":height - 1*bottom_height/3 + 5
        },
        {
            "x":2*unit/3 + 10,
            "y":height - 1*bottom_height/3 + 5
        }
    ]
    ];
    

}

function draw() {
    if (!isLoaded) {
        background(0);
        return;
    }
    clear();
    strokeWeight(1);

    line(width/2,0,width/2,height);
    stroke(0);

//    line(mouseX,0,mouseX,height);    
  //  line(0,mouseY,width,mouseY);
    line(0,unit,width,unit);
    
    textSize(18);
    knobIndex = -1;//always -1 when mouse not in knob
    buttonIndex = -1;//always -1 when mouse not in button

    for(let rowIndex = 0;rowIndex < 3;rowIndex++){
        for(let columnIndex = 0;columnIndex < 3;columnIndex++){
            strokeWeight(5);
            knob_distance = Math.sqrt( (knobs[rowIndex][columnIndex].x - mouseX)**2  + (knobs[rowIndex][columnIndex].y - mouseY)**2);
            if(knob_distance < knob_radius){
                fill("#00ff0080");
                knobIndex = rowIndex*3 + columnIndex;
              //  fill(0);
//                text(knobIndex.toString(),10,35);
            }
            else{
                fill(255);
            }
            circle(knobs[rowIndex][columnIndex].x,knobs[rowIndex][columnIndex].y,knob_size);
            fill(0);
            strokeWeight(1);
            text(qnr.knobs[rowIndex][columnIndex].toString(),knobs[rowIndex][columnIndex].x + 10,knobs[rowIndex][columnIndex].y);
            if(mouseX > buttons[rowIndex][columnIndex].x && mouseX < buttons[rowIndex][columnIndex].x + button_width && mouseY > buttons[rowIndex][columnIndex].y && mouseY < buttons[rowIndex][columnIndex].y + button_height){
                fill("#00ff0080");
            }
            else{
                fill(255);
            }
            rect(buttons[rowIndex][columnIndex].x,buttons[rowIndex][columnIndex].y,button_width,button_height);
            strokeWeight(1);
            fill(0);
            text(qnr.buttons[rowIndex][columnIndex],buttons[rowIndex][columnIndex].x +  5,buttons[rowIndex][columnIndex].y + 28);
        }
    }
    fill(0);
    text(qnr.knob_mode,10,15);
    text(qnr.display_mode,width/2  + 10,15);

    
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
