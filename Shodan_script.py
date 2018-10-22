import shodan,socket,sys,re 

sho_api_key = ''
api = shodan.Shodan(sho_api_key)

"""
Looks for a specific kind of technology or protocol
try : 
	results = api.search('ftp')
	print('[>]Number of results found:',results['total'])
	for result in results['matches'] : 
		print('\n'+'[>]IP address:',result['ip_str']+'\n')
		print('[>]result:',result['data']+'\n')

except Exception as e:
	print('[!]An exception accured:',e)
"""
def search_host(address): 
	server_info = api.host(address)
	#Target general info
	if 'latitude' in server_info.keys() and 'longitude' in server_info.keys() : 
		lat = server_info['latitude']
		lon = server_info['longitude']
	print('\n'+'[>]IP :',server_info['ip_str'],'\n'
		  '[>]Organisation :',server_info.get('org','---'),'\n'
		  '[>]OS :',server_info.get('os','---'),'\n'
		  '[>]Country-city-PostalCode :',server_info.get('country_name','None'),'-',server_info.get('city','None'),'-',\
		  server_info.get('postal_code','None'))
	if lat :
		print('[>]Latitude:',lat)
	if lon : 
		print('[>]Longitude',lon)
	#Banner and port :
	for item in server_info['data']:
		print('[>]Port',item['port'],'\n'
			  '[>]Banner',item['data'],'\n')
	#Vulns found and info : 
	if 'vulns' in server_info.keys() : 
		for vuln in server_info['vulns']:
			print('[>]Vulnerability :',vuln)
			CVE = vuln = vuln.replace('!','')
			exploits = api.exploits.search(CVE)
			for match in exploits['matches'] : 
				if match.get('cve')[0] == CVE :
					print(match.get('description'))
	else :
		pass

def main():
	host_url = input('[>]Host to parse ex: 92.56.18.103 : ')
	#try : 
	if 'https' in host_url:
		port = 443
		host_url = host_url.replace('https://','')
		ip_addr = socket.getaddrinfo(host_url,port,family=socket.AF_INET,type=socket.SOCK_STREAM)
		# To adapt for IPv6, add a try statement before the preceding line and except an error with family AF_INET6 on ip_addr var.
		for item in ip_addr:
			family,type1,proto,can,sockaddr = item 
			search_host(sockaddr[0])
	elif 'http' in host_url:
		port = 80
		host_url = host_url.replace('http://','')
		ip_addr = socket.getaddrinfo(host_url,port,family=socket.AF_INET,type=socket.SOCK_STREAM)
		# To adapt for IPv6, add a try statement before the preceding line and except an error with family AF_INET6 on ip_addr var.
		for item in ip_addr:
			family,type1,proto,can,sockaddr = item 
			search_host(sockaddr[0])
	elif re.search('https|http|www',host_url,re.I) is None : 
		search_host(host_url)
	elif re.search('https|http',host_url,re.I) is None and 'www' in host_url : 
		sys.exit('[!]Must use http/s')
	else : 
		sys.exit('[!]Not valid host.')
	#except:
		#	print('error occured')

main()