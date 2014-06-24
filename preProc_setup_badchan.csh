#/!bin/csh

#Marks bad channels in all of a subject's raw .fif datafiles from a given session
#set for use on Cephalopod
#You need to make a R####_bad_chan.txt file manually before running this script

#If your subjects didn't have anything weird happen to them, it's better to use the preProc_setup_all.csh
#script, which combines the marking bad channels and binary conversion steps. 

#run this way: ./preProc_setup.csh AUDI R1841 


setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup

cd /Volumes/CUTTLEFISH/MEG_Experiments/$1/data/$2

echo "Marking bad channels"

if ( -e $2_bad_chan.txt ) then
    foreach f ( *_raw.fif )
	mne_mark_bad_channels $f --bad $2_bad_chan.txt  
    end
endif


