import httplib
import urllib2
from xml.dom import minidom
import json

def wind(airport='CYHU'):
	site=airport.upper()
	url=urllib2.urlopen('http://gca.navcanada.ca/gca/iwv/'+site)
	url.readline() # dummy read - scrap first line
	doc=minidom.parse(url)
	data=[]
	for spanNode in doc.getElementsByTagName('span'):
		att=spanNode.getAttribute('class')
		if att == 'stat-data' or att == 'alt-normal':
			s=''
			for Node in spanNode.childNodes:
				if type(Node)==list:
					s=''.join([N.nodeValue for N in Node])
				else:
					s=Node.nodeValue
				data.append(str(s))
	keys=['dir','kt','gust','alt','datestamp']
	return dict(zip(keys,data))

def taf(loc='cyhu'):
	loc=loc.upper()
	resp=urllib2.urlopen('http://avwx.rest/api/taf/'+loc)
	tbl=resp.readlines()
	data=json.loads(tbl[0])
	taftbl=[loc]
	for line in data['Forecast']:
		taftbl.append(str(line['Raw-Line']))
	return taftbl

'''
 # <table class="data-tbl" summary="Weather Data">\n',
    # <tr class="top-data" >\n',
       # <td class="stat-cell" >\n',
          # Direction du vent:<br /><span class="stat-data" >180</span >\n',
       # </td >\n',
       # <td class="stat-cell" >\n',
          # Vitesse du vent:<br /><span class="stat-data" >17</span >\n',
       # </td >\n',
       # <td class="stat-cell" >\n',
          # Rafales<br/>Incluses:<br /><span class="stat-data" >--</span >\n',
       # </td >\n',
       # <td class="stat-cell" >\n',
          # Altim&#232;tre:<br /><span class="alt-normal">&nbsp;30.30&nbsp;</span >\n'
       # </td >\n',
       # <td class="stat-cell" >\n',
          # Mise &#224; jour:<br /><span class="stat-data" >2018-09-25 15:31:58Z</span
       # </td >\n',
    # </tr >\n',
 # </table >\n',
 

 https://www.blog.pythonlibrary.org/2010/11/12/python-parsing-xml-with-minidom/
 https://mikedesjardins.net/2007/10/04/parsing-xml-with-python-and-minidom/
 
 
 
 
 
 
 '''
 