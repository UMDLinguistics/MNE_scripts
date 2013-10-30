#!/bin/csh

#set for use on Cephalopod
#Note: 6th argument is optional
#run this way: ./sqdtxt2fif.csh AUDI R1851 AUDI_random2 1000 07.02.13 21
#e.g., experiment = AUDI, subj = R1851, paradigm = AUDI_random2,  samplingrate = 1000hz, experimentdate = 07.02.13, stimthresh = 21, **(only enter 6th argument if you wish to set a stimulus threshold deviating from default

##**IMPLICIT(not an argument)** coregistration info file from MEG160 = R1851_AUDI_random2_07.02.13-Filtered-coregis.txt

#do not rename the MEG160 coregis text file as $2_$3_coreg.txt prior to running this command or else the output overwrites the existing one but becomes blank

#if your events are triggered 'off' instead of 'on', you need to add an '--allevents' argument to the last line

setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup

cd /Users/Shared/Experiments/$1/data/$2
mkdir eve
mkdir rej
mkdir ave
mkdir cov

##extract the data's coregistration info from text file printed from MEG160 #section added by Lawrence on 07.09.13
sed -e '4,$ ! d' \
	-e '9,$ d' \
	-e 's/^	Marker [0-9]:   MEG:x=\ *//' \
	-e 's/ *\[mm].*//' \
    -e 's/\, [y-z]=//g' <KIT/$2_$3_$5-Filtered-coregis.txt >KIT/$2_$3_coreg.txt
    
setenv thresh 20

##convert the data
if ($6) then
	setenv thresh $6
endif

mne_kit2fiff --raw KIT/$2_$3_$5-Filtered-matexp.txt --elp KIT/$2_$5.elp --hpi KIT/$2_$3_coreg.txt --out $2_$3-Filtered_raw.fif --sns /Users/Shared/MNE_scripts/function_inputs/SensorsCommaKIT.txt --aligntol 100 --stim 163:164:165:166:167:168:169:170:171:172:173:174:175:176:179:180:181:182:183:184:185:186:187:188 --stimthresh $thresh --sfreq $4 --hsp KIT/$2_$5.hsp


##output a text file containing events that were read
mne_process_raw --raw $2_$3-Filtered_raw.fif --eventsout eve/$2_$3.eve --allevents


