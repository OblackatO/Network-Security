import sys,re,argparse,socket

try : 
	from scapy.all import * 
except Exception as e :
	print('[!]Is scapy installed ?')
	print('[>]Installation possible via pip : python3.x : pip3 install scapy-python3'+'\n'\
	'sudo must be used if not root')
	sys.exit('Exception details:'+str(e))

file1 = open('Open_Ports_results.txt','w')
file1.close()

VulportsTCP = [3389,22,23,5900,9999,25,79,80,443,8080,8443,8888,1433,3306,5433,2049,111,445,\
21,6001,6002,6003,6004,6005]
VUlportsUDP = [161,500,1434,53,111,137,69]
Vulnerable_Ports = {'137':'NETBIOS Name Service,UDP','111':'sunrpc - SUN Remote Procedure Call,UDP',\
'53':'Domain name system server,UDP','3389':'Remote Desktop Protocol(RDP),TCP','22':\
'Secure Shell(SSH),TCP','23':'Telnet,TCP','6000':'x11,TCP','6001':'x11,TCP','6002':'x11,TCP',\
'6003':'x11,TCP','6004':'x11,TCP','6005':'x11,TCP','5900':'Virtual Network Connector(VNC),TCP',\
'9999':'Remote administrative interface for legacy networking material,TCP'\
,'25':'SMTP,TCP','79':'Finger,TCP','161':'Simple Network Management Protocol,UDP','80':'http,TCP','443':'https,TCP'\
,'8080':'Tomcat Management Page,TCP','8443':'JBoss Management Server,TCP','8888':'System admin Panel,TCP','500':'Internet security association and key Management protocol,UDP','1433':'Microsoft Structured Query Language Server(MSSQLS),TCP',\
'1434':'SQL server browser service,UDP','3306':'MySQL,TCP','5433':'PostgressSQL server,TCP','2049':'Network File Service,TCP',\
'111':'Sun Remote Procedure Call(RPP),TCP','445':'Server Message Block(SMB),TCP','21':'FTP(File Transfer Protocol),TCP',\
'69':'Trivial File Transfer Protocol'}

def netmask_CIR_trans(netmask):
	if '255.255.255.255' in netmask : return '/32'
	elif '255.255.255.254' in netmask : return '/31'
	elif '225.255.255.252' in netmask : return '/30'
	elif '255.255.255.248' in netmask : return '/29'
	elif '255.255.255.240' in netmask : return '/28'
	elif '255.255.255.224' in netmask : return '/27'	
	elif '255.255.255.192' in netmask : return '/26'
	elif '255.255.255.128' in netmask : return '/25'
	elif '255.255.255.0' in netmask : return '/24'
	elif '255.255.254.0' in netmask : return '/23'
	elif '255.255.252.0' in netmask : return '/22'
	elif '255.255.248.0' in netmask : return '/21'
	elif '255.255.240.0' in netmask : return '/20'
	elif '255.255.224.0' in netmask : return '/19'
	elif '255.255.192.0' in netmask : return '/18'
	elif '255.255.128.0' in netmask : return '/17'
	elif '255.255.0.0' in netmask : return '/16'
	elif '255.254.0.0' in netmask : return '/15'
	elif '255.252.0.0' in netmask : return '/14'
	elif '255.248.0.0' in netmask : return '/13'	
	elif '255.240.0.0' in netmask : return '/12'	
	elif '255.224.0.0' in netmask : return '/11'
	elif '255.192.0.0' in netmask : return '/10'	
	elif '255.128.0.0' in netmask : return '/9'
	elif '255.0.0.0' in netmask : return '/8'
	elif '254.0.0.0' in netmask : return '/7'
	elif '252.0.0.0' in netmask : return '/6'
	elif '248.0.0.0' in netmask : return '/5'
	elif '240.0.0.0' in netmask : return '/4'
	elif '224.0.0.0' in netmask : return '/3'
	elif '192.0.0.0' in netmask : return '/2'
	elif '128.0.0.0' in netmask : return '/1'
	elif '0.0.0.0' in netmask : return '/0'
	else:
		sys.exit('[!]IPv4 netmask is not valid')

def IPv4_hosts(ipv4,netmask):
	internal_hosts = []
	dst = ipv4+netmask
	eth_p = Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_p = ARP(pdst=dst)
	packet = eth_p/arp_p
	resp,non_resp = srp(packet,timeout=0.5,verbose=0)
	if resp:
		print('-------------------------------------------------------------')
		print('[>]Internal network IPv4 hosts:')
		for sent,recv in resp:
			internal_hosts.append(recv[ARP].psrc)
			try:
				hostname = str(socket.gethostbyaddr(recv[ARP].psrc)[0])
				print('[>]Host:'+str(recv[ARP].psrc),'HostName:'+hostname,\
				'MAC address:'+str(recv[Ether].src))
			except:
				print('[>]Host:'+str(recv[ARP].psrc),'HostName:'+\
				'MAC address:'+str(recv[Ether].src))
		print('-------------------------------------------------------------'+'\n')
	else:
		print('[!]No hosts on the network..')
	return internal_hosts

def Port_Scanner_IPv4_TCP(host,portstcp):
	ip_p = IP(dst=host) 
	tcp_p = TCP(dport=portstcp,flags=2) # 2 == SYN flag 
	packet = ip_p/tcp_p
	resp,non_resp = sr(packet,timeout=0.5,verbose=0)
	if resp :
		for sent,recv in resp :
			if recv.haslayer(TCP):
				if recv[TCP].flags == 18: # 18 == SYN-ACK FLAG ; 16:ACK ; 2:SYN
					packet_graceful_ter = IP(dst=host)/TCP(dport=recv[TCP].sport,flags=4) #Send RST packet to terminate the connection gracefully
					send(packet_graceful_ter,verbose=0)
					sport = str(recv[TCP].sport)
					print('[>]Host:'+str(recv[IP].src),'Opened Port:'+str(recv[TCP].sport),'Service:'+str(Vulnerable_Ports[sport]))
					file1 = open('Open_Ports_results.txt','a')
					file1.write('[>]Host:'+str(recv[IP].src)+' Opened Port:'+str(recv[TCP].sport)+'  Service:'+str(Vulnerable_Ports[sport])+'\n')
					file1.close()
				else:
					pass
	else:
		pass

def Port_Scanner_IPv4_UDP(host,portudp):
	closed_ports = []
	check_pass = True
	ip_p = IP(dst=host)
	udp_p = UDP(dport=portudp)
	packet = ip_p/udp_p
	resp,non_resp = sr(packet,timeout=1,verbose=0)	
	if resp :
		for sent,recv in resp:
			if recv.haslayer(ICMP):
				closed_ports.append(portudp)
	if closed_ports == []:
		print('[>]Host:'+str(host)+'  Opened Port:'+str(portudp)+'  Service:'+str(Vulnerable_Ports[str(portudp)]))
		file1 = open('Open_Ports_results.txt','a')
		file1.write('[>]Host:'+str(host)+'  Opened Port:'+str(portudp)+'  Service:'+str(Vulnerable_Ports[str(portudp)])+'\n')
		file1.close()

			
def arguments_def():
	usage ='\n'+'This program scans the ports that are useful for a Pentration Test(To see those ports use '+sys.argv[0]+ ' -VulnPorts)\
 It scans the hosts of an entire internal network or a public IP address(domain).The type of scan is SYN-ACK scan(Sealth scan) or UDP depending on the port service, using scapy.'+'\n'+\
 'Note that many websites have filtered udp ports, in this case, the program will simply print open, but the port may not be opened.\
 see more details about filtered, open, closed ports meanings at : https://nmap.org/book/man-port-scanning-basics.html'+'\n'+\
 '----------------------------------------------------------------------'+'\n'+\
 '[OPTION]...[IP] ; examples :'+'\n'+sys.argv[0]+' -ipv4 192.118.128.22 -netmask 255.255.255.0'+'\n'+\
 sys.argv[0]+' -ipv4 192.113.123.22 -netmask 255.255.254.0 -PublicIP www.google.lu'+'\n'+\
 '-----------------------------------------------------------------------'+'\n'+\
 'If you specify an internal ipv4 the netmask must be specified.\
 All the information required to run this program can be obtained by running the script Get_SysInfo.py for python 3.x. A public and internal\
 host can be specified at the same time, like in the examples.'
	'-----------------------------------------------------------------------'+'\n'
	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument('-ipv4',type=str,help='Your internal IPv4, or any other IPv4 on the network.')
	parser.add_argument('-netmask',type=str,help='If IPv4 specified,the netmask must be specified as well.')
	parser.add_argument('-PublicIP',type=str,help='A website or its IP address.')
	parser.add_argument('-VulnPorts',help='Prints the ports that are going to be scanned.',action='store_true')
	args,unknown_args = parser.parse_known_args()
	if unknown_args:
		print('[!]Unknown arguments:',unknown_args)
	if args.VulnPorts :
		for item in Vulnerable_Ports:
			print('[>]'+str(item),':',Vulnerable_Ports[item])
		print('')
	if args.PublicIP:
		if 'www' in args.PublicIP:
			try:
				hostname = socket.gethostbyname(args.PublicIP)
			except:
				try:
					hostname = socket.getaddrinfo(args.PublicIP, 80, proto=socket.IPPROTO_TCP)
					hostname = hostname[1][4][0]
				except Exception as e:
					print('[!]If you think your link is valid, report exception to the program creator:pegom0896@gmail.com')
					sys.exit('[!]Unable to translate website to I.P address, exception details:'+str(e))
			print('\n'+'[>]Scanning host:'+str(hostname))
			Port_Scanner_IPv4_TCP(hostname,VulportsTCP)
			for port in VUlportsUDP:
				Port_Scanner_IPv4_UDP(hostname,port)
		if '.' in args.PublicIP and not 'www' in args.PublicIP:
			print('\n'+'[>]Scanning host:',args.PublicIP)
			Port_Scanner_IPv4_TCP(args.PublicIP,VulportsTCP)
			for port in VUlportsUDP:
				Port_Scanner_IPv4_UDP(args.PublicIP,port)
		print('\n'+'See Open_Ports_results.txt for results.')
	if args.ipv4 and not args.netmask : 
		sys.exit('[!]Specify netmask')
	if args.ipv4 and args.netmask : 
		for host in IPv4_hosts(args.ipv4,netmask_CIR_trans(args.netmask)):
			print('\n'+'[>]Scanning host:'+str(host))
			Port_Scanner_IPv4_TCP(host,VulportsTCP)
			for port in VUlportsUDP:
				Port_Scanner_IPv4_UDP(host,port)
		print('\n'+'See Open_Ports_results.txt for results.')

def main():
	arguments_def()

main()








"""
COMMENT 1 : Scapy for python3 may have a bug concerning IPv6 echo requests and replies, this also
affects ICMPv6ND_NA and ICMPv6ND_NS. Sometimes Scapy does not get the responses from the hosts
which means there might be hosts alive that Scapy does not tell you. For this reason one should
run tcpdump or other packet filter program to check if Scapy's really working. This only 
affects the protocol ICMPv6, and its subclasses(ICMPv6ND_NS, etc), and it does not happen always.
I posted the issue in the scapy3 dev page, but I did not get any response. I think this will 
be taken care of when IPv6 will be more used in the future. I posted this issue in the scapy2 
(for python2.7) dev page and the issue was fixed on the same day. 

COMMENT 2 : I was getting an error "unknown host" while translating the ipv6 address to 
its domain name (an internal IPv6), but when I tried to use my loopback ipv6 "::1", it worked
fine, so I suppose it is a problem with the configuration of scapy. Its ipv6 route was not configured, actually 
I had never set it, because I can work fine with ipv6 packets without it, plus when I set
the scapy ipv6 route it does not persist. I was using a router that was not using IPv6 native 
connections, I believe that this also have contributed to the error. In conclusion, this error
should not happen if you're using IPv6 native connections, and if it does, the script excepts 
it and passes it, the only difference to the user is that he won't be able to see the domain
names of the internal hosts. 

COMMENT 3 : If you see outputs such as "WARNING: more Mac address to reach destination not found. Using broadcast.
", ignore it, it should not happen with IPv6 native connections, I tried to set verbose of 
scapy to 0, but it still appearing. This only happens in IPv6, and it does not affect the 
normal execution of the program at all. 
""" 
"""
NOTE about screenshots : in pages that may have a loginpage use phantomJS
to take screenshots and even to search for login forms. See selenium folder 
and see the scripts for more information
"""
			