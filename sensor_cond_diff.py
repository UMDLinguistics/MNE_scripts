import numpy as np
import mne
import argparse

#example
#run sensor_cond_diff.py NARWHAL R1704 Narwhal_semprime 0 1

#The last two numbers are the position of the condition in the average file

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('par',type=str)
parser.add_argument('cond1',type=int)
parser.add_argument('cond2',type=int)

args=parser.parse_args()


##Filenames
data_path = '/Users/Shared/Experiments/'+args.exp+'/data/'+args.subjID + '/' #Lawrence added 'Experiments' 4.23.13
data_file = data_path + args.subjID + '_' + args.par 


evoked = mne.fiff.read_evoked(data_file +'-ave.fif',setno=[args.cond1,args.cond2])

data_diff = evoked[1].data-evoked[0].data

evoked_diff = evoked[0]
evoked_diff.data = data_diff
evoked_diff.comment = evoked[1].comment + '-' + evoked[0].comment

evoked = mne.fiff.read_evoked(data_file +'-ave.fif',setno=[args.cond1,args.cond2])
evoked.append(evoked_diff)

mne.fiff.write_evoked(data_file + '_' + str(args.cond2)+ '-' + str(args.cond1) + '-ave.fif', evoked)

