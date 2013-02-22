#/!bin/csh

#set for use on Cephalopod
#run this way: ./preProc_setup.csh AUDI R1841 


setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup

cd /Users/Shared/$1/data/$2

echo "Marking bad channels"

if ( -e $2_bad_chan.txt ) then
    foreach f ( *_raw.fif )
	mne_mark_bad_channels $f --bad $2_bad_chan.txt  
    end
endif


