from bs4 import BeautifulSoup
bsinstance = BeautifulSoup(open('ltps_parse.html'),"lxml")

#Searches for all img tags with a class on it , True means it can be any class, but one class can be specified.
classimg = bsinstance.find_all('div',class_='label_text',limit=5) #can set a limit to the number of classes you want 
for classi in classimg:
	print classi