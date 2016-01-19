import numpy as np

def minusMean(readFile,writeFile):
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

def toBin(readFile,writeFile):
	avgFeat = readMatrix(readFile,',')
	avgFeat[avgFeat>0] = 1
	avgFeat[avgFeat<0] = 0
	writeBin(writeFile,avgFeat,'')
	print 'finish toBin'

if __name__ == '__main__':
	minusMean('feature.txt','averageFeature.txt')
	toBin('averageFeature.txt','binaryCode.txt')