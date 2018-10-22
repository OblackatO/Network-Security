from bs4 import BeautifulSoup

bsinstance = BeautifulSoup(open('parse_facebook.html'),"lxml")
imgstag = bsinstance.find_all('img')
for imglink in imgstag:
	print imglink['src']


#change the src from the picture.
for imalink in imgstag:
	if 'src' in imalink.attrs:
		imalink['src'] = 'http://images.clipartpanda.com/test-clip-art-cpa-school-test.png'
	else:
		pass

result = str(bsinstance)
#create new html file to upload new changes.
htmlfile = open('final_fbPage.html','w')
htmlfile.close()

htmlfile = open('final_fbPage.html','ab')
htmlfile.write(result)
htmlfile.close()