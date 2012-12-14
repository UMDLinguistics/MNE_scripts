###SemPrMM
###Make .ave files
###usage: python <this script.py> subjectID projType
###ex: python makeAveFiles.py ya16 projoff

import sys
import condCodes as cc

def makeAveFiles(exp, subjID, paradigm):

	filePrefix = '/Users/Shared/'+exp+'/data/'+ subjID
 	magRej = "3000e-15"


	## SUBJECT-SPECIFIC REJECTION THRESHOLD MODIFICATIONS
 	# if subjID == "ya31":
#  		magRej = "4000e-15"   ##note exception for ya31 and sc9, whose magnetometers were baseline noisy


	#expList = ['SemPrime']
##    expList = ['BaleenHP'] ## changed on 9/7 for testing number of trials in each case(rej, PCA+rej, PCA+norej -CU)

	condDict = cc.condLabels
	preBase = cc.preBase
	postBase = cc.postBase
	preBasePar = preBase[paradigm]
	postBasePar = postBase[paradigm]
	print condDict[paradigm]
	print cc.epochs

	filename = filePrefix + '/ave/'+subjID + '_'  + paradigm + '.ave'
	print filename
									
	myFile = open(filename, "w") ##clears file
	myFile.close()	
			
	myFile = open(filename, "a")
	myFile.write('average {\n\n')
	myFile.write('\tname\t\"'+ exp + ' averages\"\n\n')
	myFile.write('\toutfile\t\t'+subjID+ '_' +  paradigm + '-ave.fif\n')
	myFile.write('\tlogfile\t\t./logs/'+subjID + '_' + paradigm + '-ave.log\n')
	myFile.write('\teventfile\t'+filePrefix+'/eve/'+subjID+'_' + paradigm + 'ModRej.eve\n\n')
	myFile.write('\tmagReject\t'+magRej + '\n\n')
	
	for item in condDict[paradigm]:
		print item
		#epInfo = epDictPar[item[0]]
		myFile.write('\tcategory {\n')
		myFile.write('\t\tname\t\"'+item[1]+'\"\n')
		myFile.write('\t\tevent\t'+item[0]+'\n')
		myFile.write('\t\ttmin\t-'+str(float(preBasePar)/1000)+'\n')
		myFile.write('\t\ttmax\t' + str(float(postBasePar)/1000) + '\n\t}\n\n')

									
	myFile.write('}\n')


if __name__ == "__main__":
	makeAveFiles(sys.argv[1],sys.argv[2], sys.argv[3])