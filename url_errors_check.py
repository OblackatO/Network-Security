# -*- coding: utf-8 -*-
import re, random
import urllib as ur

url = raw_input('[>]Enter url:')
tag = '<*address>'
list_postions = []

random_number = chr(random.randint(97,122)) # chr inverse of ord
url2 = url + random_number # make attention to / after the website
page_info = ur.urlopen(url2)
content = page_info.read()
if page_info.code == 404 : 
	print '[!]Detected error handling possible failure.'
	file1 = open('results.txt','a')
	file1.write('---------RESULTS---------'+'\n')
	file1.write(url2)
	file1.write('\n'+'-------------------------'+'\n')
	file1.write(content)
	file1.write('\n'+'--------------------------'+'\n')	
	for match in re.finditer(tag,content):
		start_position = match.start()
		ending_position = match.end()
		if start_position and ending_position : 
			list_postions.append(start_position)
			list_postions.append(ending_position)
	if len(list_postions) > 0 : 
		print '[>]Failure confirmed.'
		a = list_postions[1]
		b = list_postions[2]
		print content[a:b]
	else:
		print'[>]Error handling seems fine.'
if page_info.code == 200:
	print'[>]Web-site correctly handles errors'

"""
The program run very well and I had the excepected results, but 
I was not able to accomplish the same task with the urllib.request
of python3.x using the same function urlopen(). Instead of passing
the error to the var, like in python2, in python3 the error is raised
and the program breaks with its TraceBack
How this script works : 

if error code 404 : We got an error, now there are web pages 
which servers give information about them when an error occurs 
in this case we look for the tag <address> that has the information
about the kind of server that is running that webpage

if code 202 : The page handles correctly erros
"""