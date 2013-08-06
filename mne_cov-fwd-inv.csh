#!/bin/csh

#set for use on Cephalopod
#run this way: ./mne_cov-fwd-inv.csh AUDI R0253 AUDI_random2 COR-AUDI_08.01.13
#arguments: $1 = experiment, $2 = subjectID, $3 = paradigm, $4 = mri-digitizer coregistration file

setenv MNE_ROOT /Applications/MNE-2.7.4-3378-MacOSX-x86_64
source $MNE_ROOT/bin/mne_setup


cd /Users/Shared/Experiments/$1/data/$2

setenv SUBJECT $2

##create noise covariance matrix
sudo mne_process_raw --raw $2_$3-Filtered_raw.fif --projon --cov /Users/Shared/Experiments/$1/data/$2/cov/$2_$3.cov
#permission required
#if you have more than one, use something like
#mne_process_raw  --raw ../$1_MaskedMMRun1_ssp_raw.fif --raw ../$1_MaskedMMRun2_ssp_raw.fif --cov ../cov/$1_MaskedMMRun1.cov  --cov ../cov/$1_MaskedMMRun2.cov --gcov $1_MaskedMM_All-cov.fif --projon --lowpass 20

##create forward solution
mne_do_forward_solution --bem /Users/Shared/MRI/structural/fs_subjects/$2/bem/$2-5120-5120-5120-bem-sol.fif --meas $2_$3-ave.fif --mri /Users/Shared/MRI/structural/fs_subjects/$2/mri/T1-neuromag/sets/$4.fif --overwrite >>& /Users/Shared/Experiments/$1/data/$2/logs/$2_$3_makefwd.txt

##if you have more than one, use something like this:
#mne_average_forward_solutions --fwd $1_MaskedMMRun1-ave-7-$t-fwd.fif --fwd $1_MaskedMMRun2-ave-7-$t-fwd.fif --out $1_MaskedMM_All-ave-7-$t-fwd.fif

##if $2_$3-ave-7-fwd.fif already exists in the directory, you will overwrite it with the optional "--overwrite" argument; thus, if you do not want to overwrite it, manually input the mne_do_forward_solution command line without "--overwrite"

##create inverse operator
mne_do_inverse_operator --fwd $2_$3-ave-7-fwd.fif --depth --loose .2 --meg --senscov $2_$3_denoised-cov.fif >>& /Users/Shared/Experiments/$1/data/$2/logs/$2_$3_makeinv.txt
