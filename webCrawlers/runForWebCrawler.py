import requests
import codecs
import re
import json
from bs4 import BeautifulSoup
def getFromURL(url,page,name,count,pageCount):
	tmpUrl = url
	for i in range(page):
		print str(pageCount) + ' : ' + tmpUrl
		pager = requests.get(tmpUrl)
		pageSoup = BeautifulSoup(pager.content)
		count = handleThisPage(pageSoup, count, name)
		tmpUrl = 'http://list.jd.com' + pageSoup.find(class_='pn-next').get('href')
		pageCount += 1

def handleThisPage(pageSoup, count,name):
	for sp in pageSoup.find_all(class_='p-img'):
		try:
			count = handleItems(sp,count,name)
		except Exception,e:
			print e
			f = open('../data/log.txt','a')
			f.write(sp.find('a').get('href')+'\n')
			f.close()
	print 'handleThisPage'
	return count

def handleItems(sp,count,name):
	#get item url
	itemUrl = sp.find('a').get('href')
	#now itemUrl is an array
	allItemUrl = getItemColorUrl(itemUrl)
	#allItemUrl = [itemUrl]
	for itemUrl in allItemUrl:
		isGet = False
		failTimes = 0
		while (isGet == False) & (failTimes <= 5):
			try:
				count = handleThisItem(itemUrl,count,name)
				isGet = True		
			except Exception,e:
				print e
				failTimes+=1
	return count

def handleThisItem(itemUrl,count,name): 
	count = count + 1
	#get item url
	itemr = requests.get(itemUrl,timeout=10)
	itemSoup = BeautifulSoup(itemr.content)
	#picture & store
	writePic(itemSoup,'../data/pic/'+name+'/'+name+str(count))
	#get price
	price = getPrice(itemr)
	#info
	writeInfo(itemSoup,'../data/info/'+name+'/'+name+str(count)+'.txt',price,itemUrl)
	print 'pic'+str(count)+' success & url = ' + itemUrl
	return count


def getItemColorUrl(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')
	try:
		tmpHref = [item.find('a') for item in soup.find(id='choose-color').find_all(class_='item')]
		href = []
		for h in tmpHref:
			if h != None:
				href.append('http:'+h.get('href'))
	except:
		href = [url]
	return href

def writePic(itemSoup,name):
	picUrl = itemSoup.find(class_='jqzoom').find('img').get('src')[2:]
	picr = requests.get('http://'+picUrl,timeout=10)
	picf = open(name,'w')
	picf.writelines(picr.content)
	picf.close()

def writeInfo(itemSoup,name,price,itemUrl):
	infof = codecs.open(name,'w','utf-8')
	infof.write(itemUrl + '\n')
	infof.write('price : ' + price)
	try:
		for pa in itemSoup.find(id='parameter2',class_='p-parameter-list').find_all('li'):
			infof.write('\n')
			infof.write(unicode(pa.contents[0]))
	except Exception,e:
		print str(e) + ' 89th line'
	infof.close()

def getPriceFromJson(skuid):
	priceUrl = 'http://p.3.cn/prices/get?skuid=J_'+skuid
	priceJson = json.loads(requests.get(priceUrl).content)[0]
	if priceJson['p']:
		price = priceJson['p']
		return price
	else:
		return -1

def getPrice(itemr):
	skuid_re = re.compile(r'skuid: (.*?),')
	skuid = re.findall(skuid_re,itemr.content)[0]
	price = getPriceFromJson(skuid)
	return price

if __name__ == '__main__':
	#count for the num of bao which has been download
	getFromURL('http://list.jd.com/list.html?cat=1672%2C2575%2C2580&go=0',150,'bao',127135,1)#getFromURL(url,page,name,count,pageCount)
	print 'Finish!!!'
