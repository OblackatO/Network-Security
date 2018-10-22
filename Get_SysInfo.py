#!/usr/bin/env python3
import socket,platform,sys,re
import urllib.request as ur

try : 
	import netifaces
except Exception as e :
	print('[!]Is netifaces lib installed ?')
	print('[>]Installation possible via pip : python3.x : pip3 install netifaces'+'\n'\
	+'sudo must be used if not root')
	sys.exit('Exception details:'+str(e))

def InIPv4_6_Macaddr():
	eth_info,ipv4_info,ipv6_info = '','',''
	ipv6_net,ipv4_net = '',''
	internal_interfaces = netifaces.interfaces()
	for item in internal_interfaces:
		if re.search('127.0.0.1|::1',str(netifaces.ifaddresses(item))) is not None:
				print('[>]Loopback Interface is configured:',item)
				continue	
		try:
			ether_net = netifaces.ifaddresses(item)[netifaces.AF_LINK]
			ipv4_net = netifaces.ifaddresses(item)[netifaces.AF_INET]
			ipv6_net = netifaces.ifaddresses(item)[netifaces.AF_INET6] 
		except:
			try:
				ipv6_net = netifaces.ifaddresses(item)[netifaces.AF_INET6] #SEE COMMENT (1)
			except:
				pass 
		if ether_net:
			eth_info= ether_net[0]['addr']
		if ipv4_net != '':
			ipv4_info = ipv4_net[0]['addr'],ipv4_net[0]['netmask'],ipv4_net[0]['broadcast']
		if ipv6_net != '': 
			ipv6_info = ipv6_net[0]['addr']
			if "%"+item in str(ipv6_info):
				ipv6_info= ipv6_info.strip("%"+item)
		if re.search('irda',item) is not None:
			print('[>]Interface(Infrared) '+item+':')
		else:
			print('[>]Interface '+item+':')
		if eth_info != '':
			print('		MAC address:',eth_info)
		if ipv4_info != '':
			print('		IPv4 Info:','Adress:'+str(ipv4_info[0]),'Netmask:'+str(ipv4_info[1])\
			,'Broadcast:'+str(ipv4_info[2]))
		else:
			print('		IPv4 not configured...')
		if ipv6_info != '':
			print('		IPv6 Info:',ipv6_info)
		else:
			print('		IPv6 not configured...')
	if ipv4_info != '' and ipv6_info != '':
		return ipv4_info[0][0],ipv6_info
	elif ipv6_info == '' and ipv4_info != '':
		return ipv4_info[0]
	elif ipv4_info == '' and ipv6_info != '' :
		return ipv6_info
	
def OS_hostName(internal_ip):
	list_attr = ['system','Node','Release','Version','Machine'\
	,'Processor']
	dict_final = {}
	OS_info = platform.uname()
	hostname = socket.gethostbyaddr(socket.gethostname())
	for x in range(0,5):
		dict_final[list_attr[x]] = OS_info[x]
	print('[>]Machine Information:','\r')
	for key in dict_final:
		print('	[>]'+str(key),':',dict_final[key])
	print('[>]Hostname:',hostname[0])
	return internal_ip

def extIP_Domain(internal_ip):
	try:
		web_page = ur.urlopen('http://ipinfo.io/json')
		web_page = web_page.read().decode()
	except Exception as e:
		sys.exit('[!]An error occured while getting your public IP'\
			,'details:'+str(e))
	print('[>]External IP information:')
	print(web_page.strip("}").strip('{').strip('"'))
	externalip = ur.urlopen('https://myexternalip.com/raw').read().decode()
	if re.search('No hostname',web_page,re.I) is not None:
		print('[>]External IPv4 hostname:',socket.gethostbyaddr(externalip)[0])	
	if ':' not in str(internal_ip): #SEE COMMENT (2)
		print('[>]If IPv6 enable visit this website to know you public IPv6 : http://test-ipv6.com/\
		or http://ipv6-test.com/ ')
	try:
		extIP_domain = ur.urlopen('http://'+str(externalip))
		print('[>]External IP domain:',extIP_domain)
	except ur.URLError:
		print('[>]You external IP is not associated to a domain.')
	
def main():
	print('\n','		[>]...System Information...[<]		','\n')
	extIP_Domain(OS_hostName(InIPv4_6_Macaddr()))

main()


"""
COMMENT 1 : If an error occurs in ipv4_net line and if interface has IPv6 configured and not IPv4 we won't be able \
to get the IPv6 because of the "pass" statement in exception that is why I used try within except. 
It is not a very graceful way to do it, so I'm accepting suggestions ! .

COMMENT 2 : if ":" is not in the internal_ip string that means that it is an ipv4. Still
the user can also have a public IPv6 configured in the same host. In this case 
it would take several lines of code to configure the urllib to use the second available
ip (the ipv6) to make a request to the website that gives the public ip information. I could
have used scapy to make a three way handshake to the website and then make a GET request 
, but it's easier and actually less errorful if the user simply visits the website the script
prints, with its own browser. Still, in case both Ipv4 and IPv6 are configured this 
script can be configured to print the public information of both of them, but of course
a few more lines would need to be added. In case only ipv6 is configured, the urllib should
work fine with it. This script was only tested using ipv4 and ipv4/6 configured at the
same time, never with ipv6 only. 

If you have any questions or do not understand something on my code, do not hesitate to 
ask me. Any criticism specially negative/contructive is greatly appriciated ! 
"""