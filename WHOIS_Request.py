import urllib.request as ur 
from bs4 import BeautifulSoup
#import re

url = input('[>]Enter the desired URL(e.g.:rtl.lu) : ')

final_url = "https://dig.whois.com.au/whois/"+url
print(final_url)
opener = ur.urlopen(final_url)
content = opener.read().decode('utf-8')

#list_of_positions = []
#print(content.decode())
#tag_to_find = '<*pre>'
#for match in re.finditer(tag_to_find,content):
#	s = match.start()
#	e = match.end()
#	list_of_positions.append(s)
#	list_of_positions.append(e)
#whois_data = content[list_of_positions[1]:list_of_positions[2]]
#print(whois_data.replace("%",''))

Soup = BeautifulSoup(content,'html.parser')
wanted_data = Soup.find('pre')
list_to_replace = ['%','<pre>','</pre>']
for item in list_to_replace:
	wanted_data = str(wanted_data).replace(item,'')
print(wanted_data)

"""
The script uses the : https://dig.whois.com.au/whois/ to make a whois request 
to a desire website. 
Now the response and wanted data from the website can be get in two 
ways. Either using BeautifoulSoup or re libs. With Beautiful is more
straight forward and easy, still the way of doing it with re is commented with #
"""