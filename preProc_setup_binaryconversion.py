import readInput
import writeOutput
import sys

#script to convert events from binary to human-readable

def binary_conversion(exp, subjID, paradigm):

	maxCount = 16777215  #2^24-1, because we use 24 good triggers (162-187, excluding 176 and 177; could go to 188 but more than 2^24 screws MNE conversion)
	filePath = '/Volumes/CUTTLEFISH/MEG_Experiments/'+exp+'/data/' #Lawrence added 'Experiments' 4.23.13
	
	trigSeqDict = {1:162,2:163,3:164,4:165,5:166,6:167,7:168,8:169,9:170,10:171,11:172,12:173,13:174,14:175,15:178,16:179,17:180,18:181,19:182,20:183,21:184,22:185,23:186,24:187}
	
	binaryDict = {maxCount-2**0:1,maxCount-2**1:2,maxCount-2**2:3,maxCount-2**3:4,maxCount-2**4:5,maxCount-2**5:6,maxCount-2**6:7,maxCount-2**7:8,maxCount-2**8:9,maxCount-2**9:10,maxCount-2**10:11,maxCount-2**11:12,maxCount-2**12:13,maxCount-2**13:14,maxCount-2**14:15,maxCount-2**15:16,maxCount-2**16:17,maxCount-2**17:18,maxCount-2**18:19,maxCount-2**19:20,maxCount-2**20:21,maxCount-2**21:22,maxCount-2**22:23,maxCount-2**23:24}
	
	count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	
	#print binaryDict
	inFile = filePath + subjID + '/eve/' + subjID + '_' + paradigm + '.eve'
	outFile = filePath + subjID + '/eve/' + subjID + '_' + paradigm + 'Mod.eve'

	eveData = readInput.readTable(inFile)
	
	for row in eveData:
		#print row
		if (not row[3] == str(maxCount)) and (not row[3] == '0'):
			#print row
			code = binaryDict[int(row[3])]
			#print trigSeqDict[code]
			count[code-1] = count[code-1]+1
			row[3] = trigSeqDict[code]
			row[2] = 0
	
	for row in eveData:
		if row[3] == str(maxCount):
			#print 'catch'
			eveData.remove(row)
			
	writeOutput.writeTable(outFile,eveData)		
			
	print count
	i=0
	for item in count:
		i = i+1
		print "trigger_"+str(i)+" = "+str(item)

if __name__ == "__main__":
	binary_conversion(sys.argv[1],sys.argv[2],sys.argv[3])