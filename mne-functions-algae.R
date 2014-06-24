
#create dataframe for a given time-window
readQuadData <- function(expDir, expName, subjlist,epBeg, epEnd, sampleRate, t1, t2){
  fileName <- paste('/Volumes/CUTTLEFISH/MEG_Experiments/',expDir,'/results/Quadrants/',expName,'_',subjlist,'_quadTest.txt',sep="")
  quadData <- read.table(fileName)
  infoData <- quadData[1:3]
  megData <- quadData[4:length(quadData)]
  time_vector <- seq(epBeg, epEnd, 1000/sampleRate)
  sample1 <- which(time_vector == t1)
  sample2 <- which(time_vector == t2)
  winData <- rowMeans(megData[sample1:sample2])
  allWinData <-cbind(infoData,winData)
  allWinData.df <- data.frame(quad=factor(allWinData[,1]),subj=factor(allWinData[,2]),cond=factor(allWinData[,3]),amp=allWinData[,4])
  return(allWinData.df)
  
}

#create dataframe for a given time-window
readChanData <- function(expDir, expName, subjlist,epBeg, epEnd, sampleRate, t1, t2,chanLabel){
  fileName <- paste('/Volumes/CUTTLEFISH/MEG_Experiments/',expDir,'/results/',chanLabel,'/',expName,'_',subjlist,'_',chanLabel,'Test.txt',sep="")
  chanData <- read.table(fileName)
  infoData <- chanData[1:3]
  megData <- chanData[4:length(chanData)]
  time_vector <- seq(epBeg, epEnd, 1000/sampleRate)
  sample1 <- which(time_vector == t1)
  sample2 <- which(time_vector == t2)
  winData <- rowMeans(megData[sample1:sample2])
  allWinData <-cbind(infoData,winData)
  allWinData.df <- data.frame(chanGroup=factor(allWinData[,1]),subj=factor(allWinData[,2]),cond=factor(allWinData[,3]),amp=allWinData[,4])
  return(allWinData.df)
  
}

#create dataframe for a given time-window
readChanDataDiff <- function(expDir, expName, subjlist,epBeg, epEnd, sampleRate, t1, t2,chanLabel){
  fileName <- paste('/Volumes/CUTTLEFISH/MEG_Experiments/',expDir,'/results/',chanLabel,'/',expName,'_',subjlist,'_',chanLabel,'Diff.txt',sep="")
  chanData <- read.table(fileName)
  infoData <- chanData[1:3]
  megData <- chanData[4:length(chanData)]
  time_vector <- seq(epBeg, epEnd, 1000/sampleRate)
  sample1 <- which(time_vector == t1)
  sample2 <- which(time_vector == t2)
  winData <- rowMeans(megData[sample1:sample2])
  allWinData <-cbind(infoData,winData)
  allWinData.df <- data.frame(chanGroup=factor(allWinData[,1]),subj=factor(allWinData[,2]),cond=factor(allWinData[,3]),amp=allWinData[,4])
  return(allWinData.df)
  
}



#quadDataTtest('narwhal_subj_n19',-100,1000,500,800,998,'Neg','Ung')
quadDataTtest <- function(expDir, expName, subjlist,epBeg, epEnd, sampleRate, t1, t2,cond1,cond2){
  allWinData.df <- readQuadData(expDir, expName, subjlist,epBeg,epEnd,sampleRate,t1,t2)
  
  winData.LA <- subset(allWinData.df,quad=="LA")
  winData.LP <- subset(allWinData.df,quad=="LP")
  winData.RA <- subset(allWinData.df,quad=="RA")
  winData.RP <- subset(allWinData.df,quad=="RP")
  
  la_t <- tapply(winData.LA$amp,list(winData.LA$subj,winData.LA$cond),mean)
  lp_t <- tapply(winData.LP$amp,list(winData.LP$subj,winData.LP$cond),mean)
  ra_t <- tapply(winData.RA$amp,list(winData.RA$subj,winData.RA$cond),mean)
  rp_t <- tapply(winData.RP$amp,list(winData.RP$subj,winData.RP$cond),mean)
  
  la_ttest <- t.test(la_t[,cond1],la_t[,cond2],paired=TRUE)
  lp_ttest <- t.test(lp_t[,cond1],lp_t[,cond2],paired=TRUE)
  ra_ttest <- t.test(ra_t[,cond1],ra_t[,cond2],paired=TRUE)
  rp_ttest <- t.test(rp_t[,cond1],rp_t[,cond2],paired=TRUE)
  
  filePath <- paste('/Volumes/CUTTLEFISH/MEG_Experiments/',expDir,'/results/R/',sep="")
  outFileName <- paste(filePath,'t-tests/t-test_',expName,'_',subjlist,'_',cond1,'_',cond2,'_',t1,'-',t2,'.txt',sep="")
  sink(outFileName)

  print ("Quadrant T-test Results:\n")
  print("LA T-test")
  print(la_ttest)
  print("LP T-test")
  print(lp_ttest)
  print("RA T-test")
  print(ra_ttest)
  print("RP T-test")
  print(rp_ttest)
  sink()
  
  
}