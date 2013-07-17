#!/bin/csh

#set for use on Cephalopod
#run this way: ./preProc_avg.csh AUDI R1841 M100 

setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup


cd /Users/Shared/Experiments/$1/data/$2
mkdir ave
mkdir logs

mne_process_raw --raw $2_$3-Filtered_raw.fif --ave ave/$2_$3.ave --projoff --lowpass 20 


