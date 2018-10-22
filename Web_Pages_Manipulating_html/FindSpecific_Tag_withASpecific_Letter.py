from bs4 import BeautifulSoup
import re 

bsinstance = BeautifulSoup(open('parse_facebook.html'),"lxml")
#Prints every tag that has a 'b'
for tword in bsinstance.find_all(re.compile('b')): # if i wrote : re.compile('^b'): it only match tags which first letter is b 
	print tword.name