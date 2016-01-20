import Image

def loadBinaryCode(filename):
	f = open(filename,'r')
	binaryCode = []
	#get code from file
	for line in f.readlines():
		binaryCode.append(line[:-1])
	f.close()
	return binaryCode

def constructDictionary(binaryCode,segNum,bitNum):
	#array whose menber is dictionary(dicNum = segNum)
	dic = []
	bitEachSeg = bitNum / segNum
	#construct segNum dic
	for i in range(segNum):
		dic.append({})
	#insert element
	for no in range(len(binaryCode)):
		for j in range(segNum):
			bc = binaryCode[no][j*bitEachSeg:(j+1)*bitEachSeg]
			if bc not in dic[j]:
				dic[j][bc] = []
				dic[j][bc].append(no)
			else:
				dic[j][bc].append(no)
	return dic

def searchBinCode(searchCode,dic,bitAllowed,bitTotal,binaryCode):
	segNum = len(dic)
	bitEachSeg = bitTotal / segNum
	# find candidates
	candidate = []
	bitAllowedEachSeg = int(bitAllowed / segNum)
	#calculate difCode
	difCode = []
	for i in range(bitAllowed+1):
		difCode += getDifCode(bitEachSeg,bitAllowedEachSeg)
	#calculate changeCode
	for i in range(segNum):
		changeCode = getChangedCode(searchCode[i*bitEachSeg:(i+1)*bitEachSeg],difCode)
		for key in changeCode:
			candidate += dic[i][key]
	candidate = set(candidate)
	candidate = [cand for cand in candidate]
	#check whether the candidate satisfy
	final = []
	for cand in candidate:
		if diffeneceLessThanAllow(searchCode,binaryCode[cand],bitAllowed):
			print cand
			final.append(cand)
	return final

#
def getChangedCode(originalCode,difCode):
	bitNum = len(originalCode)
	#str to int
	originalCode = int(originalCode,2)
	#initial DifCode
	changeCode = [originalCode^dCode for dCode in difCode]
	#int to str
	result = [bin(originalCode)[2:]]
	return ['0'*(bitNum-len(code)) + code for code in result]

#
def getDifCode(bitTotal,bitChange):
	if bitChange == 0:
		return [0]
	if bitTotal == bitChange:
		return [2**bitTotal - 1]      
	else:
		return getDifCode(bitTotal-1,bitChange) + [code + 2**(bitTotal-1) for code in getDifCode(bitTotal-1,bitChange-1)]		

def diffeneceLessThanAllow(codeA,codeB,bitAllowed):
	count = 0
	for i in range(len(codeA)):
		if codeA[i] != codeB[i]:
			count += 1
			if count > bitAllowed:
				return False
	return True

def getThePicWithList(finalList,path,numEachFolder,nameEachFolder):
	for i in range(len(finalList)):
		#show finalList[i], i start with 0 so add 1
		finalList[i] += 1
		#count which folder should pic i belong
		count = 0
		j = 0
		while finalList[i] > (numEachFolder[j]+count):
			count += numEachFolder[j]
			j += 1
		#bug
		if finalList[i] > 4494 + count:
			finalList[i] += 1
			print 'temp bug'
		picPath = path + nameEachFolder[j] + '/' + nameEachFolder[j] + str(finalList[i] - count)
		print picPath
		im = Image.open(picPath)
		im.show()

if __name__ == '__main__':
	segNum = 64
	#get binary codes from file
	binaryCode = loadBinaryCode('binaryCode.txt')
	print 'finish load'
	#construct dictionary (bc,segNum,bitNum)
	dic = constructDictionary(binaryCode,segNum,len(binaryCode[0]))
	print 'finish construct dict'
	#searchCode
	testCode = binaryCode[0]
	finalList = searchBinCode(testCode,dic,70,1024,binaryCode)
	#find the picture's path
	nameEachFolder = ['danjianbao','shoutibao','xiekuabao']
	numEachFolder = [5721,5855,5868]
	path = '../data/pic/'
	getThePicWithList(finalList,path,numEachFolder,nameEachFolder)
