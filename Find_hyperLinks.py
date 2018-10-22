from bs4 import BeautifulSoup 
import urllib.request as ur

url = input('[>]Enter the URL:')
opener = ur.urlopen(url)
content = opener.read().decode()

Soup = BeautifulSoup(content,'html.parser')
print('[>Title:',Soup.title.text)
for link in Soup.find_all('a'):
	print(link.get('href'))

#wanted_data = Soup.find('div',id='normal')
#print(wanted_data.decode())

"""
The script opens a webpage passes its contents to the content var 
and parses it with BeautifulSoup. It finds all the a tags and gets
its contents concerning the atribute href which is the hyperlink
we're looking for, using the function .get(). 
"""