import numpy as np
import mne
import argparse

#example
#run sensor_cond_diff_ga.py NARWHAL narwhal_semprime subj_n16  0 1

#The last two numbers are the position of the condition in the average file

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('par',type=str)
parser.add_argument('subjList',type=str)
parser.add_argument('cond1',type=int)
parser.add_argument('cond2',type=int)

args=parser.parse_args()


##Filenames
data_path = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/results/'
data_file = data_path + args.par + '_' + args.subjList + '_ga'


evoked = mne.fiff.read_evoked(data_file +'-ave.fif',setno=[args.cond1,args.cond2])

data_diff = evoked[1].data-evoked[0].data

evoked_diff = evoked[0]
evoked_diff.data = data_diff
evoked_diff.comment = evoked[1].comment + '-' + evoked[0].comment

evoked = mne.fiff.read_evoked(data_file +'-ave.fif',setno=[args.cond1,args.cond2])
evoked.append(evoked_diff)

mne.fiff.write_evoked(data_file + '_' + str(args.cond2)+ '-' + str(args.cond1) + '-ave.fif', evoked)

