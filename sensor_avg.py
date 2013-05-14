import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import readInput
import pprint, pickle

#to run script, type: ipython [this python file name] [experiment name ('exp')] [subject ID ('subjID')] [paradigm ('par')] [name of file containing the experiment's dictionary('expCondDict')] [name of file containing channels of interest ('chan_filename')] [condition(s) ('condList'); separate multiple conditions with space]
#example
#ipython sensor_avg.py AUDI R1524 AUDI_blocked AUDI_R1524_blocked_Bark9_topSourceM100.txt Bark8 Bark9 Bark10 Bark11 

#The last number is the position of the condition in the average file

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('par',type=str)
parser.add_argument('expCondDict',type=str, help='file contains the experiment condition dictionary; include file extension')
parser.add_argument('chan_filename',type=str,help='file contains the channels of interest; include file extension')
parser.add_argument('condList',type=str,nargs='+',help='condition name will be converted to an integer')
#parser.add_argument('chans',type=int,nargs='+',help='enter channel number separated by space in between)
parser.add_argument('--rms',action='store_true',help='optional argument: it does root-mean-square of data')
parser.add_argument('-b','--baseline',help='optional argument: name the baseline condition to give it a thicker plot line')

args=parser.parse_args()


if args.baseline:
	if args.baseline not in args.condList:
		sys.exit("Error: Baseline condition does not exist. It must be from condList")


##Condition dictionary

dict_file = open('/Users/Shared/Experiments/'+args.exp+'/'+args.expCondDict, 'rb')
condDict = pickle.load(dict_file)
pprint.pprint(condDict)
dict_file.close()

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


##Plotting condition(s)
for cond in args.condList:
	
	condName = cond
	print "Processing {}...".format(condName)
	condCode = condDict[cond]
	print "{} is converted {} for python indexing".format(condName, condCode)
	
	evoked = mne.fiff.Evoked(data_file +'-ave.fif',setno=condCode, baseline=(None,0))
	
	meg_data = evoked.data
	times = evoked.times*1000
	
	print meg_data
	print chans
	print meg_data[chans]
	
	data_to_plot = meg_data[chans]

	# optional rms:
	if args.rms:
		data_to_plot = np.sqrt(np.mean(meg_data[chans]**2,0))
		print "root-mean-square applied"
	else:
		data_to_plot = np.mean(meg_data[chans],0)
		print "no root-mean-square applied"
	
    # optional baseline:
	
	if args.baseline==condName: # Baseline condition gets extra thick line
		plt.plot(times,data_to_plot,linewidth=3)
	else:
		plt.plot(times,data_to_plot)
	
	#plt.legend(args.condList, loc='best') ## adding legend can work inside and outside the loop
	print "Processing {} complete".format(condName)


plt.legend(args.condList, loc='best')
plt.grid(True)
plt.axhline(linewidth=1,color='k')
plt.axvline(linewidth=1,color='k')
plt.xlabel('Time (millisecond)')
plt.ylabel('Magnetic Amplitude (Tesla)')

plt.show()
print "All done!"