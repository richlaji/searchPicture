import numpy as np
import random
import time
from readAndWrite import *

def afterMinusAverage(readFile,writeFile):
	fr = open(readFile,'r')
	#store total feature
	feature = []
	path = []
	for line in fr.readlines():
		tmpFeat = [float(a) for a in line.split(' ')[2:-1]]
		feature.append(tmpFeat)
		path.append(line.split(' ')[0].split('/')[-1])
	writePath('path.txt', path)
	#now the type of feature is np.matrix
	feature = minusAverage('mean.txt',feature)
	writeMatrix(writeFile,feature,',')

def minusAverage_old(filename,feature):
	feature = np.matrix(feature)
	average = []
	row = feature.shape[0]
	time1 = time.time()
	#calculate the mean and minus
	for i in range(feature.shape[1]):
		avg = sum(feature[:,i])[0,0] / row 
		average.append(avg)
		feature[:,i] = feature[:,i] - avg
		if (i+1) % 8 == 0: 
			time2 = time1
			time1 = time.time()
			print i,time1-time2
	writeMatrix(filename,average,',')
	return feature

def minusAverage(filename,feature):
	feature = np.matrix(feature)
	average = []
	row = feature.shape[0]
	time1 = time.time()
	#calculate the mean and minus
	for i in range(feature.shape[1]):
		sumOfCol = 0
		for j in range(row):
			sumOfCol += feature[j,i]
		average.append(sumOfCol / row)
		feature[:,i] = feature[:,i] - sumOfCol / row
		if (i+1) % 8 == 0: 
			time2 = time1
			time1 = time.time()
			print i,time1-time2
	writeMatrix(filename,average,',')
	return feature	

def toBin(readFile,writeFile,rorateMatrix):
	avgFeat = readMatrix(readFile,',')
	R = readMatrix(rorateMatrix,',')
	avgFeat = np.matrix(np.dot(avgFeat,R))
	avgFeat[avgFeat>0] = 1
	avgFeat[avgFeat<0] = 0
	writeBin(writeFile,avgFeat,'')
	print 'finish toBin'

def itq(times,V):
	#print 'V is '
	#print V
	R = np.random.random((V.shape[1],V.shape[1]))
	S,O,St = np.linalg.svd(R)
	#initial
	R = St.T
	#B = np.matrix(np.random.random((V.shape[0],V.shape[1])))
	for i in range(times):
		#Fix R
		time1 = time.time()
		B = np.dot(V,R)
		B[B>=0] = 1
		B[B<0] = -1
		#Fix B
		#print np.dot(B.T,V)
		S,O,St = np.linalg.svd(np.dot(B.T,V))
		R = np.dot(St.T,S.T)
		time2 = time.time()
		print i,time2-time1
	writeMatrix('R.txt',R,',')

def getTotalLine(filename):
	f = open(filename,'r')
	lines = len(f.readlines())
	f.close()
	return lines

def itqTrain(trainNum,averageFeatureFileName):
	#get totalNum & percent
	totalNum = getTotalLine(averageFeatureFileName)
	print 'totalNum is :' + str(totalNum)
	percent = float(trainNum)/float(totalNum)
	print 'itq training percent is : ' + str(percent)
	#read
	averageFeature = readMatrixWithPercent(averageFeatureFileName,',',percent)
	itq(50,averageFeature)
	print 'finish itq training'

if __name__ == '__main__':
	#average
	#afterMinusAverage('feature.txt','averageFeature.txt')
	#itq
	#itqTrain(10000,'averageFeature.txt')
	#bin
	toBin('averageFeature.txt','binaryCode.txt','R.txt')