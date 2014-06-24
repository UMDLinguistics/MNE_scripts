## Comprehension Evaluation for LindyHop
# For use with Matlab logs of SentMEG experiments.

##Import Modules ##
import argparse
import os

## Define the function ##

def eval_LH(expt, subjID, paradigm):

# Set the paths
	
	
	filepath = '/Users/Shared/Experiments/'+args.expt+'/data/'+args.subjID+'/KIT'
    
	origFile = filepath+ '/' +args.subjID+ '_' +args.paradigm+ '.log'
	midwayFile = filepath+ '/' +args.subjID+ '_' +args.paradigm+ '_midway.txt'
	score= filepath+ '/' +args.subjID+ '_' +args.paradigm+ '_score.txt'
	
	
#extract question and response lines from original logfile
#and print to a new midway file
    
	f1 = open(origFile, 'r')
	f2 = open(midwayFile, 'w')
	ls1 = f1.readlines()
	lines = [l.split('\t') for l in ls1]
 	
 
	for i, line in enumerate(lines):
		if (('155' in line[2]) | ('156'in line[2])):
			f2.write(' '.join(lines[i]))
			f2.write(' '.join(lines[i + 1]))

	f1.close()
	f2.close()
    
	print 'Halfway through!'

#evaluate button presses
	f2 = open(midwayFile, 'r')
	f3= open(score,'w')
	ls2 = f2.readlines()
	lines = [l.split() for l in ls2]


	for i in range(len(lines)-1):
		ln1= lines[i]
		ln2= lines[i+1]


		if (('156' in ln1[2:]) & ('y' in ln2)):
			f3.write('1\n')
			
		elif (('156' in ln1[2:]) & ('g' in ln2)):
			f3.write('0\n')
			
		elif (('155' in ln1[2:]) & ('g' in ln2)):
			f3.write('1\n')
				
		elif (('155' in ln1[2:]) & ('y' in ln2)):
			f3.write('0\n')
		


	f2.close()
	f3.close()
	
                        	
	f3 = open(score,'r')
	lines = f3.readlines()
	correctcount = 0
	incorrectcount = 0
	total = 0

	
	for row in lines:
		if (row == '1\n'):
			correctcount += 1
			total += 1
			
		elif (row == '0\n'):
			incorrectcount += 1
			total += 1
			
	print correctcount		
	print incorrectcount
	print total
	
	finalScore = (round((float(correctcount)/float(total)), 3))*100
	
	f3.close()
	print ('The subject scored: ' + str(finalScore) + '%') 
	f3 = open(score,'a')
	f3.write('Final Score: ' + str(finalScore) + '%')

	print("Done?")

#########################################
### Main function ###

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get input')
	parser.add_argument('expt',type=str)
	parser.add_argument('subjID',type=str)
	parser.add_argument('paradigm',type=str)
	args=parser.parse_args()
  
  	eval_LH(args.expt, args.subjID, args.paradigm)
  	
print "Totally done!"
	

 
