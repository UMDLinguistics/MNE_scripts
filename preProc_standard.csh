#!/bin/csh

###Run all standard pre-processing steps automatically, after conversion to fif is complete
###Call like this: ./preProc_standard.csh NARWHAL narwhal_semprime_subj_n23.txt Narwhal_semprime


foreach line (`cat /Volumes/CUTTLEFISH/MEG_Experiments/$1/subjLists/$2`)
	echo $line
	./preProc_setup_all.csh $1 $line $3

	python rej_fif2blink.py $1 $line $3

	python makeAveFiles.py $1 $line $3

	./preProc_avg.csh $1 $line $3


end



