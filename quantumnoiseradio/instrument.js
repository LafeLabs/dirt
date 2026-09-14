const debug_mode = true;//set to false to send data over socket
let socket = null;
if (!debug_mode) {
  socket = new WebSocket('ws://localhost:6502');
}

knobIndex = -1;//always -1 when mouse not in knob
buttonIndex = -1;//always -1 when mouse not in button

knobClicks = 24;

let qnr = {};
let isLoaded = false;

audio_frequency_A = 220;
audio_frequency_B = 440;
audio_amplitude_A = 0.5;
audio_amplitude_B = 0.5;

var soundFile, mic, osc,fft;
var analyzer;
var numSamples = 1024;
// Array of amplitude values (-1 to +1) over time.
var samples = [];
var currentSource = "mic";
oscon = false;


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
  mic = new p5.AudioIn();
  mic.start();
  //analyzer.setInput(mic);
    
  fft = new p5.FFT();
  fft.setInput(mic);
    

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

  //  line(mouseX,0,mouseX,height);    
//    line(0,mouseY,width,mouseY);
    line(width/2,unit,width,unit);
    
    textSize(18);
    knobIndex = -1;//always -1 when mouse not in knob
    buttonIndex = -1;//always -1 when mouse not in button

    for(let rowIndex = 0;rowIndex < 3;rowIndex++){
        for(let columnIndex = 0;columnIndex < 3;columnIndex++){
            knob_distance = Math.sqrt( (knobs[rowIndex][columnIndex].x - mouseX)**2  + (knobs[rowIndex][columnIndex].y - mouseY)**2);

            if(knob_distance < knob_radius){
                knobIndex = rowIndex*3 + columnIndex;
                fill(0);
                strokeWeight(1);
                text(qnr.knobs[rowIndex][columnIndex].toString(),knobs[rowIndex][columnIndex].x + 10,knobs[rowIndex][columnIndex].y);    
                fill("#00ff0080");

            }
            else{
                fill(255);
            }
            strokeWeight(5);
            
            circle(knobs[rowIndex][columnIndex].x,knobs[rowIndex][columnIndex].y,knob_size);
            line(knobs[rowIndex][columnIndex].x,knobs[rowIndex][columnIndex].y,knobs[rowIndex][columnIndex].x + knob_radius*Math.sin(2*Math.PI*qnr.knobs[rowIndex][columnIndex]/knobClicks),knobs[rowIndex][columnIndex].y - knob_radius*Math.cos(2*Math.PI*qnr.knobs[rowIndex][columnIndex]/knobClicks));
            fill(0);
            strokeWeight(1);
            
            if(mouseX > buttons[rowIndex][columnIndex].x && mouseX < buttons[rowIndex][columnIndex].x + button_width && mouseY > buttons[rowIndex][columnIndex].y && mouseY < buttons[rowIndex][columnIndex].y + button_height){
                fill("#00ff0080");
            }
            else{
                fill(255);
            }
            rect(buttons[rowIndex][columnIndex].x,buttons[rowIndex][columnIndex].y,button_width,button_height,5);
            strokeWeight(1);
            fill(0);
            text(qnr.buttons[rowIndex][columnIndex],buttons[rowIndex][columnIndex].x +  5,buttons[rowIndex][columnIndex].y + 28);
        }
    }
    fill(0);
    text(qnr.knob_mode,10,15);
    
    if(qnr.knob_mode == "audio_out"){
        
        audio_frequency_A = qnr.audio_out.frequency_A + 100*qnr.knobs[0][0] + 10*qnr.knobs[0][1] + qnr.knobs[0][2];
        audio_frequency_B = qnr.audio_out.frequency_B + 100*qnr.knobs[1][0] + 10*qnr.knobs[1][1] + qnr.knobs[1][2];        
        
        audio_frequency_B = qnr.audio_out.frequency_B + 100*qnr.knobs[1][0] + 10*qnr.knobs[1][1] + qnr.knobs[1][2];        
        
        text("frequency_A = "  + audio_frequency_A.toString() + " Hz",10,32);
        text("frequency_B = "  + audio_frequency_B.toString() + " Hz",10,unit/2 - knob_radius - 32);
        
        text("Amplitude A = "  + audio_amplitude_A.toString(),50,5*unit/6 - knob_radius - 32);
        text("Amplitude B = "  + audio_amplitude_B.toString(),50 + 2*unit/3,5*unit/6 - knob_radius - 32);    
        
        fill(255);
        stroke(255);
        circle(knobs[2][1].x,knobs[2][1].y,knob_size + 10);
    }
    
    stroke(0);
    fill(0);
    text(qnr.display_mode,width/2  + 10,15);
    spectrum = fft.analyze();
    nyquistFreq = sampleRate() / 2;
    binFreq = nyquistFreq / (spectrum.length);

    beginShape();
    vertex(width/2,height);
    stroke(0);
    strokeWeight(1);
    noFill();
    //frequency = binFreq*i
    //
    startIndex = Math.round(qnr.audio_spectrum.start_frequency/binFreq)
    stopIndex = Math.round(qnr.audio_spectrum.stop_frequency/binFreq)
    
    for (let i = 0; i < spectrum.length; i++) {
        vertex(map(i,startIndex,stopIndex,0.5*width,width), map(spectrum[i], 0, 255, height,height - bottom_height));
    }
    vertex(width,height);
    endShape();
    
    fill(0);
    
    for(let index = 0;index < qnr.audio_spectrum.grid_lines.length;index++){

        lineIndex = Math.round(qnr.audio_spectrum.grid_lines[index]/binFreq);
        lineX = map(lineIndex,startIndex,stopIndex,0.5*width,width);
        fkhz = Math.round(qnr.audio_spectrum.grid_lines[index]/1000);
        line(lineX,height,lineX,height - bottom_height);
        text(fkhz + " kHz",lineX + 5,height - bottom_height + 20);        
    }
}

function mouseWheel(event) {
    if(knobIndex >= 0){
        if(event.delta < 0){ 
            qnr.knobs[Math.floor(knobIndex/3)][knobIndex%3]++;
        }
        else{
            qnr.knobs[Math.floor(knobIndex/3)][knobIndex%3]--;
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
