##This script creates a grand-average across subject averages and outputs to new fif
##Note this is for visualization only; doesn't take bad channels into account
##You need to make a subject list text file, one subject code per row

import numpy as np
import mne
import argparse
import sys
import copy
import readInput
import collections

#example: run sensor_grand_avg.py NARWHAL narwhal_subj_n9 Narwhal_semprime 



###########################################################################

##Get input
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('exp',type=str)
parser.add_argument('subjList',type=str)
parser.add_argument('par',type=str)

args=parser.parse_args()

##Get the condCode information
sys.path.insert(0,'/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp + '/')
fileName =args.exp+'_condCodes'
print fileName
cc = __import__(fileName) ##importing condCodes


##Initialize path variables and read subject list
expPath = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/'
data_path = expPath + 'data/'
results_path = expPath +'results/'

subjList = readInput.readList(expPath + 'subjLists/' + args.subjList+'.txt')	


##create structure for mne python to call all the conditions up
labelList = cc.condLabels[args.par]
# dictionary from trigger to condition sorted by trigger number
event_id = collections.OrderedDict(sorted(labelList, key=lambda item : item[0]))
print event_id

numCond = len(event_id)
#initialize structures needed to create grand average
allData = [ [] for item in range(numCond) ]  ##channel x time MEG data
allNave = [ [] for item in range(numCond) ]  ##number of trials per condition in ave


###################################################################################
##Loop through each subject and grab data
for subj in subjList:
	data_file = data_path + subj + '/' + subj + '_' + args.par 
	evokeds = [mne.fiff.read_evoked(data_file + '-ave.fif', setno=event_id[cond]) for cond in event_id]
	
	###add to the grand-average structures
	#evokedTemplate = []
	#evokedTemplate.append(evokeds)

	for c in range(numCond):
		allData[c].append(evokeds[c].data)
		allNave[c].append(evokeds[c].nave) 
		

#################################################################################
#Now compute grandaverage data and sum all of the n for each subject
gaveData = [np.mean(allData[cond],0) for cond in range(numCond)]
gaveNave = [np.sum(allNave[cond],0) for cond in range(numCond)]

##Make a template to fill the grand-average info into
data_file = data_path + subjList[0] + '/' + subjList[0] + '_' + args.par 
evokeds = [mne.fiff.read_evoked(data_file + '-ave.fif', setno=event_id[cond]) for cond in event_id]
newEvoked = copy.deepcopy(evokeds)

#fit this summary data into template structure
for c in range(numCond):
	newEvoked[c].data = gaveData[c]
	newEvoked[c].nave = gaveNave[c]
	
################################################################################
##Write to file

mne.fiff.write_evoked(results_path + args.subjList + '_' + 'ga' + '-ave.fif', newEvoked)

