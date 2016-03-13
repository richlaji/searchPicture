def deleteDuplicate(readfile, writefile, duplicateFile):
	#open file
	fr = open(readfile, 'r')
	fw = open(writefile, 'w')
	fd = open(duplicateFile, 'w')
	
	#handle duplicate
	dic = {}
	#insert the binCode & delete duplicate
	count = 0
	for line in fr.readlines():
		count += 1
		if not dic.has_key(line[:-1]):
			dic[line[:-1]] = []
		dic[line[:-1]].append(count)
		if count % 1000 == 0:
			print count
	#delete
	print "start writing..."
	for k in dic.keys():
		#write withoutDuplicate
		fw.write(k)
		fw.write('\n')
		#duplicate File
		for i in dic[k]:
			fd.write(str(i))
			fd.write(',') 
		fd.write("\n")
	print "end writing!"
	#close file
	fr.close()
	fw.close()
	fd.close()

if __name__ == '__main__':
	deleteDuplicate('binaryCode.txt', 'binaryCode_withoutDuplicate.txt', 'duplicateFile.txt')