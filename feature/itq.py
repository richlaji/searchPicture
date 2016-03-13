import numpy as np
import time
import PCA
def sgn(v):
	if v >= 0:
		return 1
	else:
		return -1

def preRead(X,W):
	return np.matrix(np.dot(X,W))

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
		if i % 5 == 0:
			print i
		#	writeBinaryCode(B,'B' + str(i) + '.txt')
		#	PCA.writeMatrix(R,'R' + str(i) + '.txt')
	#writeBinaryCode(B,'B.txt')
	PCA.writeMatrix(R,'R.txt')
	return 
		

def writeBinaryCode(mat,filename):
	f = open(filename,'w')
	mat = np.matrix(mat)
	for i in range(mat.shape[0]):
		for j in range(mat.shape[1]):
			if mat[i,j] > 0:
				f.write('1')
			else:
				f.write('0')
		f.write('\n')
	f.close()

def getBinaryCode(mat,meanfile):
	binaryCode = []
	f = open(meanfile,'r')
	line = f.readline()
	mean = [float(a) for a in line.split(',')]
	for i in range(mat.shape[0]):
		tmp = ''
		for j in range(mat.shape[1]):
			if mat[i,j] - mean[j] > 0:
				#tmp.append(1)
				tmp += '1'
			else:
				#tmp.append(0)
				tmp += '0'
		binaryCode.append(tmp)
	f.close()
	return binaryCode

def estimateBinaryCode(filename):
	f = open(filename,'r')
	a = np.random.random((64))
	count = 0
	for code in f.readlines():
		code = code.split('\n')[0]
		for i in range(len(code)):
			a[i] += int(code[i])
			#print int(code[i])
		count += 1
		if count % 2000 == 0:
			print count
	a /= count
	print a
	f.close()