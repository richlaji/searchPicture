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

#first start from 0
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

#second
def getFinalListWithDuplicate(finalList, duplicateFile):
	f = open(duplicateFile,'r')
	lines = f.readlines()
	finalListWithDuplicate = []
	for i in finalList:
		print i
		print lines[int(i)]
		for num in lines[int(i)].split(',')[:-1]:
			finalListWithDuplicate.append(int(num))
	print finalListWithDuplicate
	return finalListWithDuplicate

#third
def getThePicWithList(finalList,path,pathFile):
	f = open(pathFile, 'r')
	lines = f.readlines()
	for i in finalList:
		picPath = path + lines[i][:-1]
		print picPath
		im = Image.open(picPath)
		im.show()

#def tmp():
if __name__ == '__main__':
	segNum = 64
	#get binary codes from file
	binaryCode = loadBinaryCode('binaryCode_withoutDuplicate.txt')
	print 'finish load'
	#construct dictionary (bc,segNum,bitNum)
	dic = constructDictionary(binaryCode,segNum,len(binaryCode[0]))
	print 'finish construct dict'
	#searchCode
	testCode = '1100000011010110101000111101100011110110110011000110011010111010010000001011101100100101000001101011000100111010100011110000110000100100010000111111110000110001011001001000011111100000110011110011100010000011101101001000101011001001000010110100110001110001011000001011001001101010001101011100000100110000000101100000110101100110111110000000000000010110000010010001010110101010101010100100110100101111100111100101111110011110111000111101110111000011101001011110001000000101110000110101010011000101101101010011000111111100111101110111010001011010001110001000110000000111111010000000010010110000011011110101011111000101111010001011000111001111010010001100111100100101100000101011001010101010101111000111001011000110001011101010011110100011001111111001000111010001011001101110101111110110110110111000101010110100101000010111001110010000011110100001000010001110010100011111001000001111111100111110001100101100111100001000111000010001110000111001000001110111101111000100101011101011010101111010001110001101011010111000001100100010'
	finalList = searchBinCode(testCode,dic,10,1024,binaryCode)
	#find the picture's path
	#nameEachFolder = ['danjianbao','shoutibao','xiekuabao']
	#numEachFolder = [5721,5855,5868]
	finalList = getFinalListWithDuplicate(finalList, 'duplicateFile.txt')
	path = '../data/pic/bao/'
	getThePicWithList(finalList,path,'path.txt')

def test():
#if __name__ == '__main__':
	nameEachFolder = ['danjianbao','shoutibao','xiekuabao']
	numEachFolder = [5721,5855,5868]
	finalList = [1]
	path = '../data/pic/'
	getThePicWithList(finalList,path,numEachFolder,nameEachFolder)