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
			count = handleThisItem(sp,count,name)
		except Exception,e:
			print e
			f = open('../data/log.txt','a')
			f.write(sp.find('a').get('href')+'\n')
			f.close()
	print 'handleThisPage'
	return count

def handleThisItem(sp,count,name):
	#get item url
	itemUrl = sp.find('a').get('href')
	#now itemUrl is an array
	allItemUrl = getItemUrl(itemUrl)
	#allItemUrl = [itemUrl]
	for itemUrl in allItemUrl:
		itemr = requests.get(itemUrl)
		itemSoup = BeautifulSoup(itemr.content)
		#picture & store
		count = count + 1
		writePic(itemSoup,'../data/pic/'+name+'/'+name+str(count))
		#get price
		price = getPrice(itemr)
		#info
		writeInfo(itemSoup,'../data/info/'+name+'/'+name+str(count)+'.txt',price,itemUrl)
		print 'pic'+str(count)+' success & url = ' + itemUrl
	return count

def getItemUrl(url):
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
	picr = requests.get('http://'+picUrl)
	picf = open(name,'w')
	picf.writelines(picr.content)
	picf.close()

def writeInfo(itemSoup,name,price,itemUrl):
	infof = codecs.open(name,'w','utf-8')
	infof.write(itemUrl + '\n')
	infof.write('price : ' + price)
	for pa in itemSoup.find(id='parameter2',class_='p-parameter-list').find_all('li'):
		infof.write('\n')
		infof.write(unicode(pa.contents[0]))
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
	getFromURL('http://list.jd.com/list.html?cat=1672,2575,5257&page=103&go=0&JL=6_0_0',100,'bao',22079,103)
	print 'Finish!!!'