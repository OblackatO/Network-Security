from bs4 import BeautifulSoup

bsinstance = BeautifulSoup(open('parse_facebook.html'),"lxml")

for link in bsinstance.find_all(id='email'): #Can also specify a class : find_all('img',id='nightpic'); or specify another attribute
	print link 

