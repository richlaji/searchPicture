import requests
import codecs
import re
import json
import urllib
from bs4 import BeautifulSoup
def getFromURL(url,page,name):
	tmpUrl = url
	count = 0
	for i in range(page):
		pager = requests.get(tmpUrl)
		pageSoup = BeautifulSoup(pager.content)
		count = handleThisPage(pageSoup, count, name)
		tmpUrl = 'http://list.jd.com' + pageSoup.find(class_='pn-next').get('href')

def handleThisPage(pageSoup, count,name):
	for sp in pageSoup.find_all(class_='p-img'):
		try:
			count = handleThisItem(sp,count,name)
			print 'pic'+str(count)+' success & url = ' + sp.find('a').get('href')
		except Exception,e:
			f = open('../data/log.txt','a')
			f.write(sp.find('a').get('href')+'\n')
			f.close()
	return count

def handleThisItem(sp,count,name):
	#get item url
	itemUrl = sp.find('a').get('href')
	itemr = requests.get(itemUrl)
	itemSoup = BeautifulSoup(itemr.content)
	#picture & store
	count = count + 1
	writePic(itemSoup,'../data/pic/'+name+'/'+name+str(count))
	#get price
	price = getPrice(itemr)
	#info
	writeInfo(itemSoup,'../data/info/'+name+'/'+name+str(count)+'.txt',price,itemUrl)
	return count

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
	priceUrl = 'http://p.3.cn/prices/mgets?skuIds=J_'+skuid+'&type=1'
	priceJson = json.load(urllib.urlopen(priceUrl))[0]
	#print priceJson.json()
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