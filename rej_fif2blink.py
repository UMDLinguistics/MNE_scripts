###rej_fif2blink.py
###This script is meant to replace the rej_fif2blinkrej.m Matlab script; it also calls rej_rej2eve.py at the end for convenience

###Reads in a raw fif file
###Writes out rejection files, each with two columns.
###First column is time point (in samples) and next is
###channel on which that time point should be rejected (legacy)

##Ex: python rej_fif2blink.py NARWHAL R1905 Narwhal_semprime

###Uses a step rejection method. For every time sample, you take the mean of the RMS of the blink channels
###in the 100ms before the sample and the mean in the 100ms after the sample. You take the difference
###between these two numbers, and compare it against this threshold. This method discriminates long-lasting
###blinks that need to be rejected from brief, higher-frequency blips that do not.

###Default threshold is 3e-13; if you want to use a different one for your subject, save a text file 
###In that subject's data directory called /rej/rej_thr.txt
###The file should contain one line that looks like this: blink 4e-13

###Default blink channels are listed below; if you want to use a different set for your subject, 
###save a text file in that subject's data directory called /rej/R####_rej_chan.txt, in same format
###as the bad_chan.txt file

import os.path
import numpy as np
import mne
from mne import fiff
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import readInput
import writeOutput


##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('par',type=str)

args=parser.parse_args()

##Define data file names
data_path = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/data/'+args.subjID + '/' 
raw_fname = data_path + args.subjID + '_' + args.par + '-Filtered_raw.fif'
outfile_fname = data_path + 'rej/' + args.subjID + '_' + args.par + '-Filtered_raw_blink.txt'
badChan_fname = data_path + args.subjID + '_bad_chan.txt'


##Define default parameters
thresh = 3e-13
blinkChanList = [0, 1, 2, 21, 22, 23, 24, 41, 42, 43, 44, 59, 60, 61, 62, 63, 82, 83, 84, 100] # starts at 0 for python
winSize = 100  #ms on each side of test sample


##Read in a subject-specific threshold, if it exists
if os.path.isfile(data_path + 'rej/rej_thr.txt'):
	thrString = readInput.readList(data_path + 'rej/rej_thr.txt')
	thrList = thrString[0].split()
	thresh = float(thrList[1])

print
print 'Threshold used is:',thresh
print


##Read in raw data (158 channels x time samples)
raw = fiff.Raw(raw_fname)
ch_names = raw.info['ch_names']


##Read in a subject-specific blink-channel list, if it exists
if os.path.isfile(data_path + 'rej/' + args.subjID + '_rej_chan.txt'):
	blinkChanFileName = data_path + 'rej/' + args.subjID + '_rej_chan.txt'
	blinkChanStr = readInput.readList(blinkChanFileName)
	blinkChanList = []
	for blinkChan in blinkChanStr:
		ind = ch_names.index(blinkChan)
		blinkChanList.append(ind)


##Get rid of any bad channels in blink channel list (a little baroque because you have to convert from channel names to indices)
badChanStr = readInput.readList(badChan_fname)
badChanList = []
for badChan in badChanStr:
	ind = ch_names.index(badChan)
	badChanList.append(ind)

blinkChanGood = [val for val in blinkChanList if val not in badChanList] #magic python code for intersecting lists

print 
print 'blink channels: ', blinkChanList
print 'bad channels: ', badChanList
print 'rejection channels: ', blinkChanGood
print


##Extract data containing good blink channels only
blink_data, times = raw[blinkChanGood,:]

##Take the RMS
blink_data_rms = np.sqrt(np.mean(blink_data**2,0))


####################
##Compute the test value for each time point and create list of rejected samples
####################

sampRate = raw.info['sfreq']
numSamples = len(blink_data_rms)
winSizeSamp = int(winSize * (float(sampRate)/float(1000)))  ##This gives you a window size of 100ms
badSampleList = []

##You should only check samples 100ms from beginning/end of file, to have the full window
samples2Check = range(winSizeSamp,len(times)-winSizeSamp) 

for currSample in samples2Check:
	preWinMean = np.mean( blink_data_rms[currSample-winSizeSamp : currSample] )	
	postWinMean = np.mean( blink_data_rms[currSample : currSample+winSizeSamp] ) 

	stepTest = postWinMean - preWinMean    
	
	if stepTest > thresh or stepTest < -thresh:
		badSample = currSample 
		badSampleList.append([badSample,3]) #The 3 should be deprecated once we fully shift to this script
		

##Write out text file containing rejected samples
writeOutput.writeTable(outfile_fname, badSampleList)
print
print 'Artifact rejection complete'
print

##Run rej_blink2eve.py which applies the rejected samples to marking rejected epochs in eve file

import rej_blink2eve
rej_blink2eve.main(args.exp, args.subjID, args.par)


##Make a plot of the RMS
cm = plt.get_cmap('cool') # this chooses the colors to use for data lines
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(times[0:50000],blink_data_rms[0:50000],linewidth=2)
plt.title('blink rms signal for first 50,000 samples')
fig.savefig(data_path + 'rej/' + args.subjID + '_' + args.par +'blink_chan_rms.png')



