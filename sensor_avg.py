import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt


#example
#run sensor_avg.py NARWHAL R1704 Narwhal_semprime 7

#The last number is the position of the condition in the average file

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('par',type=str)
parser.add_argument('cond',type=int) # Bark9, i have input 7
parser.add_argument('chans',type=int,nargs='+')

args=parser.parse_args()

print args.chans
##args.chan = args.chan -1  ##this accounts for python indexing at 0


##Filenames
data_path = '/Users/Shared/Experiments/'+args.exp+'/data/'+args.subjID + '/' #Lawrence added 'Experiments' 4.23.13
data_file = data_path + args.subjID + '_' + args.par 

print data_path
print data_file

evoked = mne.fiff.Evoked(data_file +'-ave.fif',setno=args.cond)

meg_data = evoked.data

print meg_data
print meg_data[args.chans]

data_to_plot = meg_data[args.chans] #if i say 83, i mean 84
data_to_plot = np.mean(meg_data[args.chans],0)

plt.plot(data_to_plot)
plt.show()