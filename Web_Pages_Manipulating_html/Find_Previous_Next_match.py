from bs4 import BeautifulSoup
bsinstance = BeautifulSoup(open('ltps_parse.html'),"lxml")


#How to find strings with the string argument = bsinstance, in this case on link tags. DID NOT WORK 
links = bsinstance.find_all('meta',string='LTPS') #The string is the comments or the description
for link in links:
	print link 

#Sets a limit to searches : 
links = bsinstance.find_all('link',limit=5) 
for link in links:
	print link

#find next or preceded match of the current one, e.g:
currentmatch = bsinstance.find('link',rel="stylesheet")  
previousmatch = currentmatch.find_previous_sibling('link') # if siblings, will match all previous matches, if word link is changed, other previous tags can be found
nextmatch = currentmatch.find_next_sibling('link')
print 'Current match:'+str(currentmatch)
print 'Previous match:'+str(previousmatch )
print 'Next Match:'+str(nextmatch)