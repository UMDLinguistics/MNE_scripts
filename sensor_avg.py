import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import readInput
import sys

#to run script, type: ipython [this python file name] [experiment name ('exp')] [subject ID ('subjID')] [paradigm ('par')] [name of file containing the experiment's dictionary('expCondDict')] [name of file containing channels of interest ('chan_filename')] [condition(s) ('condList'); separate multiple conditions with space]
#example
#ipython sensor_avg.py AUDI R1524 AUDI_blocked AUDI_cond AUDI_R1524_blocked_Bark9_topSinkM100amplitude Bark8 Bark9 Bark10 Bark11 Bark12 Bark13 Bark14 Bark15

#You can optionally add arguments to do rms ("--rms") and/or thicken one of the condition lines for better visual ("-b [condition name]" or "--baseline [condition name]")

##Get input
parser = argparse.ArgumentParser(description='Description: sensor_avg.py creates a plot of MEG activity estimates from selected channels (averaged together) for selected conditions')
parser.add_argument('exp',type=str,help='enter name of experiment')
parser.add_argument('subjID',type=str,help='enter subject ID')
parser.add_argument('par',type=str,help='enter name of paradigm')
parser.add_argument('expCondDict',type=str,help='enter name of python file containing the experiment condition dictionary; do NOT include file extension; ****name of the dictionary in python script MUST be "condDict"; ****the values for the keys must correspond to the order the keys appeared in the *.ave (and *-ave.fif) files. For example, the category "Bark2_3" is first in "R1524_AUDI_blocked_bin2.ave" so its value in condDict is 0 (Python begins indexing at 0, not 1).')
parser.add_argument('chan_filename',type=str,help='enter name of text file containing the channels of interest; do NOT include file extension')
parser.add_argument('condList',type=str,nargs='+',help='enter name of condition(s) of interest; separate multiple conditions with space')
parser.add_argument('--rms',action='store_true',help='optional argument: it does root-mean-square of data')
parser.add_argument('-b','--baseline',help='optional argument: name the baseline condition to make it visually stand out; condition must be one entered for condList')

args=parser.parse_args()


if args.baseline:
	if args.baseline not in args.condList:
		sys.exit("Error: Baseline condition does not exist. It must be from condList")


##Import condition dictionary
dict_file = open('/Users/Shared/Experiments/'+args.exp + '/' + args.expCondDict + '.py', 'rb')
exec(dict_file.read())

##Filenames
data_path = '/Users/Shared/Experiments/'+args.exp+'/data/'+args.subjID + '/'
data_file = data_path + args.subjID + '_' + args.par 

print data_path
print data_file

chans = readInput.readList(data_path+'/sensor_list/'+args.chan_filename+'.txt')
chans = [int(chan) for chan in chans]
print "actual chans as shown in MNE: {}".format(chans)

chans = [chan-1 for chan in chans] # this accounts for python indexing at 0
print "chans as interpreted by iPython: {}".format(chans)


##Plot condition(s)
cm = plt.get_cmap('cool') # this chooses the colors to use for data lines
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_color_cycle([cm(1.*i/len(args.condList)) for i in range(len(args.condList))])
for cond in args.condList:
	
	condName = cond
	print "Processing {}...".format(condName)
	condCode = condDict[cond]
	print "{} is converted {} for python indexing".format(condName, condCode)
	print "NOTE: index value should correspond to the order in which the condition categories appears in {}_{}.ave. If it does not, correct it in {}.py".format(args.subjID, args.par, args.expCondDict)
	
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
		ax.plot(times,data_to_plot,linewidth=4, linestyle='--')
	else:
		ax.plot(times,data_to_plot,linewidth=2)
	
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