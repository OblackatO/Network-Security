from bs4 import BeautifulSoup

bsinstance = BeautifulSoup(open('parse_facebook.html'),"lxml")


#get text of entire html or tag : 
for link in bsinstance.find_all('script'):
	linktxt = link.get_text()
	print linktxt