# noisecube.py
# get noisecube.json
# open web socket on port 6502
# listen for commands from knobs
# set the values of DS345, HP audio synth, WindFreak A, B, or
# programmable attenuator or sdr parameters
# get noise traces 
# pass noise traces over to the front end at noisecube.js via web socket
# that is all, saving json happens from the front end automatically based on full stacks of spectra 
# if it is in simulation mode it will just compute a trace and pass it back
# it passes back the fghz or fkhz waves
