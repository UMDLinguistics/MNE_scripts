function matsqd_txt(expName, subjID, paradigmName)

%Data needs to be stored in
%/Users/Shared/Experiments/expName/data/subjID/KIT
%Example 
%matsqd_txt('NARWHAL', 'R2118','Narwhal_semprime_06.10.14-Filtered');

inPath = strcat('/Volumes/CUTTLEFISH/MEG_Experiments/',expName,'/data/',subjID,'/KIT/');
inFile = strcat(inPath,subjID,'_',paradigmName)

data = sqdread(strcat(inFile,'.sqd'));
data(:,1:157) = data(:,1:157)*1e-15;  %%return to Tesla, but don't rescale trigger lines

outFile = strcat(inFile,'-matexp.txt')
dlmwrite(outFile,data,'\t');