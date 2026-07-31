const canvas =
document.getElementById(
"midiVisualizer"
);


const ctx =
canvas.getContext("2d");


canvas.width=500;
canvas.height=120;


let note=0;


function animate(){

ctx.clearRect(
0,
0,
canvas.width,
canvas.height
);


ctx.fillRect(
50,
120-note,
40,
note
);


requestAnimationFrame(
animate
);

}


animate();



if(navigator.requestMIDIAccess){

navigator.requestMIDIAccess()

.then(access=>{


for(
let input of access.inputs.values()
){

input.onmidimessage =
(event)=>{


note =
event.data[1];


OroboroMind.think(
"MIDI "+note
);


};


}


});


}