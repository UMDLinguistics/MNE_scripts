import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import readInput
import sys
sys.path.append("/Users/Shared/Experiments/AUDI/")
import AUDI_cond as expCond

#to run script, type: ipython [this python file name] [experiment name ('exp')] [subject ID ('subjID')] [paradigm ('par')] [name of file containing channels ('chan_filename')] [condition(s) ('condList'); separate multiple conditions with space]
#example
#ipython sensor_avg.py AUDI R1524 AUDI_blocked AUDI_R1524_blocked_Bark9_topSourceM100.txt Bark8 Bark9 Bark10 Bark11 

#The last number is the position of the condition in the average file

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('par',type=str)
parser.add_argument('chan_filename',type=str,help='include file extension')
parser.add_argument('condList',type=str,nargs='+',help='condition name will be converted to an integer')
#parser.add_argument('chans',type=int,nargs='+',help='enter channel number separated by space in between)
parser.add_argument('--rms',action='store_true',help='optional argument: it does root-mean-square of data')
#things to add: (1) pickle module so we don't have to import AUDI_cond for everyone, (2) x and y = 0 axes for plot, and (3) legends for each condition on plot

args=parser.parse_args()


##Filenames
data_path = '/Users/Shared/Experiments/'+args.exp+'/data/'+args.subjID + '/'
data_file = data_path + args.subjID + '_' + args.par 

print data_path
print data_file


chans = readInput.readList(data_path+args.chan_filename)
chans = [int(chan) for chan in chans]
print "actual chans as shown in MNE: {}".format(chans)

chans = [chan-1 for chan in chans] # this accounts for python indexing at 0
print "chans as interpreted by iPython: {}".format(chans)

for cond in args.condList:
	
	condName = cond
	print "Processing {}...".format(cond)
	cond = expCond.condDict[cond]
	print "{} is converted {} for python indexing, which is the new cond".format(condName, cond)
	
	evoked = mne.fiff.Evoked(data_file +'-ave.fif',setno=cond, baseline=(None,0))
	
	meg_data = evoked.data
	times = evoked.times*1000
	
	print meg_data
	print chans
	print meg_data[chans]
	
	data_to_plot = meg_data[chans]
	
	if args.rms:
		data_to_plot = np.sqrt(np.mean(meg_data[chans]**2,0))
		print "root-mean-square applied"
	else:
		data_to_plot = np.mean(meg_data[chans],0)
		print "no root-mean-square applied"
	
	plt.plot(times,data_to_plot)
	#plt.legend(args.condList, loc='best') ## adding legend can work inside and outside the loop
	print "Processing {} complete".format(condName)


plt.legend(args.condList, loc='best')
plt.show()
print "All done!"