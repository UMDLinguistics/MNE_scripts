import numpy as np
import mne
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import readInput
import writeOutput
import sys
import Image

#to run script, type: ipython [this python file name] [experiment name ('exp')] [subject list ('subjList')] [paradigm ('par')] [name of file containing channels of interest ('chan_filename')] [condition(s) ('condList'); separate multiple conditions with space]
#example
#python sensor_avg_quad_plot.py NARWHAL narwhal_semprime_subj_n20 Narwhal_semprime "Unrelated Targets" "Related Targets" AUDI R1851 AUDI_random2 AUDI_R1851_random2_Bark_all_topSinkM100amplitude Bark6 Bark7 Bark5 Bark8 Bark9 Bark4 Bark10 Bark3 Bark2
#use "run" instead of "ipython" command if you are running this within ipython

#You can optionally add arguments to do rms ("--rms") and/or thicken one of the condition lines for better visual ("-b [condition name]" or "--baseline [condition name]")

##Get input
parser = argparse.ArgumentParser(description='Description: sensor_avg_quad.py creates a plot of MEG activity estimates from selected channels (averaged together) for selected conditions')
parser.add_argument('exp',type=str,help='enter name of experiment')
parser.add_argument('filename',type=str,help='enter grand_avg_filename')
parser.add_argument('par',type=str,help='enter name of paradigm')
parser.add_argument('condList',type=str,nargs='+',help='enter name of condition(s) of interest; separate multiple conditions with space')
parser.add_argument('--rms',action='store_true',help='optional argument: it does root-mean-square of data')
parser.add_argument('-b','--baseline',help='optional argument: name the baseline condition to make it visually stand out; condition must be one entered for condList')

args=parser.parse_args()

#plot boundaries, in Tesla
ymin = -1e-13
ymax = 1e-13

if args.baseline:
	if args.baseline not in args.condList:
		sys.exit("Error: Baseline condition does not exist. It must be from condList")


##Filenames
data_path = '/Volumes/CUTTLEFISH/MEG_Experiments/'+args.exp+'/results/'
data_file = data_path + args.filename + '_' + 'ga' 



print data_path
print data_file

quadList = ['LA','LP','RA','RP']

for quad in quadList: ########## 

	args.chan_filename = '/Volumes/CUTTLEFISH/MNE_scripts/function_inputs/quad-'+quad+'.txt'
	plot_out= data_path+'Quadrants/'+args.filename+'_'+quad+'.png' #individual plots
	

	chans = readInput.readList(args.chan_filename)
	chans = [int(chan) for chan in chans]
	#print "actual chans as shown in MNE: {}".format(chans)
	
	#chans = [chan-1 for chan in chans] # this accounts for python indexing at 0
	print "chans as interpreted by iPython: {}".format(chans)
	
	
	##Plot condition(s)
	cm = plt.get_cmap('cool') # this chooses the colors to use for data lines
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_color_cycle([cm(1.*i/len(args.condList)) for i in range(len(args.condList))])
	for cond in args.condList:
		
		condName = cond
		print "Processing {}...".format(condName)
		evoked = mne.fiff.Evoked(data_file +'-ave.fif',setno=str(condName), baseline=(None,0)) #str() for setno reassures that condName is a string so mne-python would not confuse it with dataset ID number (integer), in case the condName is a number
		
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
	plt.xlabel('Time (ms)')
	plt.ylabel('Magnetic Field Strength (Tesla)')
	plt.ylim([ymin, ymax])
	plt.title(quad)
	
	#plt.show()
	fig.savefig(plot_out)
	
## Create compiled image of the four quadrant plots
uberplot_out= data_path+'Quadrants/'+args.filename+'_quadrants.png'
LA_plot = Image.open(data_path+'Quadrants/'+args.filename+'_LA.png')
RA_plot = Image.open(data_path+'Quadrants/'+args.filename+'_RA.png')	
LP_plot = Image.open(data_path+'Quadrants/'+args.filename+'_LP.png')	
RP_plot = Image.open(data_path+'Quadrants/'+args.filename+'_RP.png')	

blank_image = Image.new ('RGB', (1600, 1200))

blank_image.paste(LA_plot, (0,0))
blank_image.paste(RA_plot, (800,0))
blank_image.paste(LP_plot, (0,600))
blank_image.paste(RP_plot, (800,600))
blank_image.save(uberplot_out)

print "Your image is ready!!"

print "All done!"