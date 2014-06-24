## Comprehension Evaluation for NARWHAL
# For use with Matlab logs of SentMEG experiments.

## Comprehension Evaluation for NARWHAL
# For use with Matlab logs of SentMEG experiments.

##Import Modules ##
import argparse
import os

## Define the function ##

def eval_NARWHAL(subjID, expt, paradigm, hand):

	filepath = '/Users/Shared/Experiments/'+args.expt+'/data/'+args.subjID+'/matlab_logs'
    
	origFile = filepath+ '/' +args.subjID+ '_' +args.paradigm+ '.log'
	midwayFile = filepath+ '/' +args.subjID+ '_' +args.paradigm+ '_midway.txt'
	score= filepath+ '/' +args.subjID+ '_' +args.paradigm+ '_score.txt'
	
#extract question and response lines from original logfile
#and print to a new midway file
    
	f1 = open(origFile, 'r')
	f2 = open(midwayFile, 'a')
	ls1 = f1.readlines()
	lines = [l.split('\t') for l in ls1]
	
	for i, line in enumerate(lines):
		if (('148' in line[2]) | ('149'in line[2])):
			f2.write(' '.join(lines[i]))
			f2.write(' '.join(lines[i + 1]))
			
	f1.close()
	f2.close()
    
#evaluate button presses
	f2 = open(midwayFile, 'r')
	f3= open(score,'w')
	ls2 = f2.readlines()
	lines = [l.split() for l in ls2]
	
	for i in range(len(lines)-1):
		ln1= lines[i]
		ln2= lines[i+1]
		
		if (hand == 'R'):
			if (('148' in ln1[2:]) & ('y' in ln2)):
				f3.write('correct\n')
                
			elif (('148' in ln1[2:]) & ('g' in ln2)):
				f3.write('incorrect\n')
			
			elif (('149' in ln1[2:]) & ('g' in ln2)):
				f3.write('correct\n')
                    
			elif (('149' in ln1[2:]) & ('y' in ln2)):
				f3.write('incorrect\n')

		if (hand == 'L'):
			if (('148' in ln1[2:]) & ('g' in ln2)):
				f3.write('correct\n')

			elif (('148' in ln1[2:]) & ('y' in ln2)):
				f3.write('incorrect\n')
                
			elif (('149' in ln1[2:]) & ('y' in ln2)):
				f3.write('correct\n')
               
			elif (('149' in ln1[2:]) & ('g' in ln2)):
				f3.write('incorrect\n')

	f2.close()
	f3.close()
                                                
#count number of correct responses

	f3 = open(score,'r')
	lines = f3.readlines()
	correctcount = 0
	incorrectcount = 0
	total = 0
	
	for row in lines:
		if (row == 'correct\n'):
			correctcount += 1
			total += 1
			
		elif (row == 'incorrect\n'):
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
	
#########################################
### Main function ###

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get input')
	parser.add_argument('subjID',type=str)
	parser.add_argument('expt',type=str)
	parser.add_argument('paradigm',type=str)
	parser.add_argument('hand',type=str)
	args=parser.parse_args()
  
  	eval_NARWHAL(args.subjID, args.expt, args.paradigm, args.hand)
  	
print "Totally done!"


 
