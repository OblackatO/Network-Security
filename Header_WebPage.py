import urllib.request as ur

url = input('[>]Enter the URL:')

opener = ur.urlopen(url)
if opener.code == 200 :
	print('[>]Header of URL:')
	print(opener.headers)


"""
Simple script that prints the header of a webpage
"""