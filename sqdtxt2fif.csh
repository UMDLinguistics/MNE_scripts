#!/bin/csh

#set for use on Cephalopod
#run this way: ./sqdtxt2fif.csh AUDI R1841 M100 1000
#e.g., experiment = AUDI subj=R1841, paradigm=M100,  samplingrate = 1000hz

#if your events are triggered 'off' instead of 'on', you need to add an '--allevents' argument to the last line

setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup

cd /Users/Shared/Experiments/$1/data/$2  #Elizabeth added 'Experiments' 4.23.13
mkdir eve

##convert the data
mne_kit2fiff --raw KIT/$2_$3-Filtered-matexp.txt --elp KIT/$2.elp --hpi KIT/$2_$3_coreg.txt --out $2_$3-Filtered_raw.fif --sns /Users/Shared/MNE_scripts/function_inputs/SensorsCommaKIT.txt --aligntol 100 --stim 163:164:165:166:167:168:169:170:171:172:173:174:175:176:179:180:181:182:183:184:185:186:187:188 --stimthresh 20 --sfreq $4 --hsp KIT/$2.hsp

##output a text file containing events that were read
mne_process_raw --raw $2_$3-Filtered_raw.fif --eventsout eve/$2_$3.eve --allevents


