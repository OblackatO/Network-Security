from bs4 import BeautifulSoup
bsinstance = BeautifulSoup(open('parse_facebook.html'),"lxml")



#completely removes and destrois a tag from the html code: 
for img in bsinstance.find_all('img'):
	img.decompose() #removes each img tag found, if i had written : imgtag = img.extract() : The tag will be taken out of the html code and equaled to the var. 

print str(bsinstance)
