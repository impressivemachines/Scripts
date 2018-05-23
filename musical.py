# python code to find out what set of dividers give an accurate set of N=12 frequencies for a top
# octave musical note generator.
# there are a bunch of print statements that can be uncommented to output various things
# this script is optimized to show the master clock frequencies that give the lowest percent error over the 11
# note frequncies that are derived from it.

# arguments are scan_master_freq_start, scan_master_freq_end, [octave_number]

import math
import numpy as np
import sys

ESC_HON = '\33[1m'
ESC_HOFF = '\33[22m'

ESC_RED = '\33[31m'
ESC_BLUE = '\33[34m'
ESC_PINK = '\33[35m'
ESC_DEF = '\33[39m'

SEPLINE = '-------------------------------------------------------------'

print()
print(ESC_HON + "Divide chain optimizer for top octave musical note generation" + ESC_HOFF)
f_start = 400000
f_end = f_start + 200000
f_delta = 10 # search step

if len(sys.argv)==2:
    f_start = int(sys.argv[1])
    f_end = f_start + f_delta
    
if len(sys.argv)>2:
    f_start = int(sys.argv[1])
    f_end = int(sys.argv[2])
    if f_end<f_start:
        print("Error: start and end frequencies are invalid")
        exit(1)
    elif f_end==f_start:
        f_end = f_start + f_delta
  
start_octave = 6  
if len(sys.argv)>3:
    so = int(sys.argv[3])
    if so<0 or so>10:
        print("Error: start octave is out of range, default =", start_octave)
        exit(1)
    start_octave = so
    
notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
N = len(notes)

note_first_hz = 1760.0 * pow(2.0, start_octave - 6) # frequency of note 'A' in Hz

f_target = np.empty(N)

# here we generate the equal interval note frequencies above note_first_hz
for index, name in enumerate(notes):
    if index>2:
        octave = start_octave+1
    else:
        octave = start_octave
    freq = note_first_hz * math.pow(2.0, index / float(N))
    #print(index, name + str(octave), "\t", round(freq,2))
    f_target[index] = freq
    
low_err = 1.0
print(SEPLINE)
print("Scanning from f_osc =",f_start,"Hz to f_osc =",f_end,"Hz")

for f_osc in range(f_start,f_end,f_delta):
    max_err_ratio = 0
    max_bits = 0
    for f in f_target:
        div = f_osc / f
        divint = int(round(div))
        bits = int(math.ceil(math.log(divint,2.0)))
        max_bits = max(max_bits, bits)
        actual_f = f_osc/float(divint)
        delta_f = abs(actual_f - f)
        err_ratio = delta_f/f
        #print(f, divint, actual_f, delta_f, round(err_ratio*100,6),'%')
        max_err_ratio = max(max_err_ratio, err_ratio)
    
    #print(f_osc,"Error =", round(max_err_ratio*100,6),"%, Divide =" , max_bits)
    #print(f_osc, max_err_ratio*100)
    if low_err > max_err_ratio:
        low_err = max_err_ratio
        best_f = f_osc
    
print(ESC_RED+"Lowest error found =",round(low_err*100,6),"%, using f_osc =",best_f,"Hz"+ESC_DEF)

print(SEPLINE)
print("Summary")
print(SEPLINE)    
f_osc = best_f # here you can just assign f_osc to whatever you like to get the info about that source freq
# f_osc = 10000000 # 10MHz clock example

for index, f in enumerate(f_target):
    if index>2:
        octave = start_octave+1
    else:
        octave = start_octave
    div = f_osc / f
    divint = int(round(div))
    actual_f = f_osc/float(divint)
    delta_f = abs(actual_f - f)
    err_ratio = delta_f/f
    print(ESC_PINK + notes[index] + str(octave) + ESC_DEF,"\tdesired =",round(f,2), "Hz\t"+ESC_BLUE+"divide = ",divint, ESC_DEF+"\toutput =",round(actual_f,2), "Hz\terror =", round(err_ratio*100,6),'%')
print(SEPLINE)

exit(0)