import numpy as np
import random

def writePath(filename,paths):
	f = open(filename,'w')
	for path in paths:
		f.write(path)
		f.write('\n')
	f.close()
	print 'finish write ' + filename

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