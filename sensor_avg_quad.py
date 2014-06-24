#import all the libraries needed for this code
import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import readInput
import sys
import writeOutput
import os


#to run script, type: python [this python file name] [experiment name ('exp')] [subject ID List ('subjList')] [paradigm ('par')] [name of file containing channels of interest ('chan_filename')] [condition(s) ('condList'): separate multiple conditions with space]
#example
#python sensor_avg_quad.py NARWHAL narwhal_semprime_subj_n16 narwhal_semprime "Unrelated Targets" "Related Targets"
#python sensor_avg_quad.py NARWHAL narwhal_subj_n19 Narwhal "Neg ever" "Factive ever" "Ungram ever"
#use "run" instead of "python" command if you are running this within ipython

#You can optionally add arguments to do rms ("--rms") and/or thicken one of the condition lines for better visual ("-b [condition name]" or "--baseline [condition name]")

##Get input
parser = argparse.ArgumentParser(description='Description: sensor_avg_quad.py creates a text file of MEG activity estimates from selected channels (averaged together) for selected conditions for further analysis in R')
parser.add_argument('exp',type=str,help='enter name of experiment')
parser.add_argument('subjList',type=str,help='enter name of subject list')
parser.add_argument('par',type=str,help='enter name of paradigm')
parser.add_argument('condList',type=str,nargs='+',help='enter name of condition(s) of interest; separate multiple conditions with space')
parser.add_argument('--rms',action='store_true',help='optional argument: it does root-mean-square of data')
parser.add_argument('-b','--baseline',help='optional argument: name the baseline condition to make it visually stand out; condition must be one entered for condList')

args=parser.parse_args()

#Make directory for all quadrant files created herafter. This command will create it if it does not already exist in your results directory.

newdirname ='/Volumes/CUTTLEFISH/MEG_Experiments/NARWHAL/results/Quadrants'

try:
	os.makedirs(newdirname)
except OSError:
	if os.path.exists(newdirname):
		pass
		print 'Quadrant directory already exists.'
	else:
		raise
		print 'There was a problem creating the quadrant directory'
		
print 'Quadrant directory ready for action.'


#plot boundaries, in Tesla
ymin = -1e-13
ymax = 1e-13

if args.baseline:
	if args.baseline not in args.condList:
		sys.exit("Error: Baseline condition does not exist. It must be from condList")


##Filenames

filename = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/results/Quadrants/'+args.par+'_'+args.subjList+'_'+'quadTest.txt'
myFile = open(filename, "w")
myFile.close()	

quadList = ['LA','LP','RA','RP']


subjList = readInput.readList('/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp + '/subjLists/'+ args.subjList + '.txt')
print subjList[0]

for subj in subjList:
	#initialize structure to hold data for each condition
	quadData = {}
	for cond in args.condList:
		quadData[cond] = []

	data_path = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/data/'+subj + '/'
	data_file = data_path + subj + '_' + args.par 
	print data_file

	quadCount = 0
	for quad in quadList:
	
		args.chan_filename = '/Volumes/CUTTLEFISH/MNE_scripts/function_inputs/quad-'+quad+'.txt'
	
		chans = readInput.readList(args.chan_filename)
		chans = [int(chan) for chan in chans]
		
		print "chans as interpreted by iPython: {}".format(chans)
			
	
		for cond in args.condList:
			
			condName = cond
			print "Processing {}...".format(condName)
			evoked = mne.fiff.Evoked(data_file +'-ave.fif',setno=str(condName), baseline=(None,0)) #str() for setno reassures that condName is a string so mne-python would not confuse it with dataset ID number (integer), in case the condName is a number
			
			meg_data = evoked.data
			times = evoked.times*1000
			
			#print meg_data
			#print chans
			#print meg_data[chans]
			
			#data_to_save = meg_data[chans]
			
			# optional rms:
			if args.rms:
				data_to_save = np.sqrt(np.mean(meg_data[chans]**2,0))
				print "root-mean-square applied"
			else:
				data_to_save = np.mean(meg_data[chans],0)
				print "no root-mean-square applied"
			
			quadData[cond].append(data_to_save)
			
			print "Processing {} complete".format(condName)
		
		
		quadCount = quadCount + 1
		print "All done!"
		
	#print quadData
	
	myFile = open(filename, "a")
	
	for cond in quadData:
		print cond
		quadCountW = 0
		for quadRow in quadData[cond]: 
			myFile.write(quadList[quadCountW])
			myFile.write("\t")
			myFile.write(subj)
			myFile.write("\t")
			myFile.write(cond.replace(" ", "_"))
			myFile.write("\t")
			for item in quadRow:
				myFile.write(str(item))
				myFile.write("\t")
			myFile.write("\n")
			quadCountW = quadCountW + 1

myFile.close()
	