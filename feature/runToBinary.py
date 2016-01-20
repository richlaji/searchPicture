import numpy as np
import random
import time

def afterMinusAverage(readFile,writeFile):
	fr = open(readFile,'r')
	#store total feature
	feature = []
	for line in fr.readlines():
		tmpFeat = [float(a) for a in line.split(' ')[2:-1]]
		feature.append(tmpFeat)
	#now the type of feature is np.matrix
	feature = minusAverage('mean.txt',feature)
	writeMatrix(writeFile,feature,',')

def minusAverage(filename,feature):
	feature = np.matrix(feature)
	average = []
	row = feature.shape[0]
	#calculate the mean and minus
	for i in range(feature.shape[1]):
		avg = sum(feature[:,i])[0,0] / row 
		average.append(avg)
		feature[:,i] = feature[:,i] - avg
		if i % 8 == 0:
			print i
	writeMatrix(filename,average,',')
	return feature

def writeMatrix(filename,mat,token):
	f = open(filename,'w')
	mat = np.matrix(mat)
	for i in range(mat.shape[0]):
		for j in range(mat.shape[1]):
			f.write(str('%.8f' % mat[i,j]))
			f.write(token)
		f.write('\n')
	f.close()
	print 'finish write ' + filename 

def writeBin(filename,mat,token):
	print 'start write Bin'
	f = open(filename,'w')
	mat = np.matrix(mat)
	for i in range(mat.shape[0]):
		for j in range(mat.shape[1]):
			f.write(str('%1.0f' % mat[i,j]))
			f.write(token)
		f.write('\n')
	f.close()
	print 'finish write ' + filename 

def readMatrix(filename,token):
	f = open(filename,'r')
	mat = []
	for line in f.readlines():
		tmpFeat = [float(a) for a in line.split(token)[:-1]]
		mat.append(tmpFeat)
	f.close()
	return np.matrix(mat)

def readMatrixWithPercent(filename,token,percent):
	f = open(filename,'r')
	mat = []
	count = 0
	for line in f.readlines():
		#if percent is 1 then all will be chosen
		if random.random() <= percent:
			tmpFeat = [float(a) for a in line.split(token)[:-1]]
			mat.append(tmpFeat)
			count += 1
	f.close()
	print 'choose num is : ' + str(count)
	return np.matrix(mat)

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