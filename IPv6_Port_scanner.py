import argparse,sys,time,socket

try : 
	from scapy.all import * 
except Exception as e :
	print('[!]Is scapy installed ?')
	print('[>]Installation possible via pip : "pip install scapy"'+'\n'\
	'sudo must be used if not root')
	sys.exit('Exception details:'+str(e))

file1 = open('Open_Ports_results.txt','w')
file1.close()

VulportsTCP = [3389,22,23,5900,9999,25,79,80,443,8080,8443,8888,1433,3306,5433,2049,111,445,\
21,6001,6002,6003,6004,6005]
VUlportsUDP = [161,500,1434,53,111,137]
Vulnerable_Ports = {'137':'NETBIOS Name Service,UDP','111':'sunrpc - SUN Remote Procedure Call,UDP',\
'53':'Domain name system server,UDP','3389':'Remote Desktop Protocol(RDP),TCP','22':\
'Secure Shell(SSH),TCP','23':'Telnet,TCP','6000':'x11,TCP','6001':'x11,TCP','6002':'x11,TCP',\
'6003':'x11,TCP','6004':'x11,TCP','6005':'x11,TCP','5900':'Virtual Network Connector(VNC),TCP',\
'9999':'Remote administrative interface for legacy networking material,TCP'\
,'25':'SMTP,TCP','79':'Finger,TCP','161':'Simple Network Management Protocol,UDP','80':'http,TCP','443':'https,TCP'\
,'8080':'Tomcat Management Page,TCP','8443':'JBoss Management Server,TCP','8888':'System admin Panel,TCP','500':'Internet security association and key Management protocol,UDP','1433':'Microsoft Structured Query Language Server(MSSQLS),TCP',\
'1434':'SQL server browser service,UDP','3306':'MySQL,TCP','5433':'PostgressSQL server,TCP','2049':'Network File Service,TCP',\
'111':'Sun Remote Procedure Call(RPP),TCP','445':'Server Message Block(SMB),TCP','21':'FTP(File Transfer Protocol),TCP'}

global hosts
hosts = []

def Discover_hosts():
	#ff02::1 -- for hosts but not routers
	ipv6_p = IPv6(dst='ff02::1')
	icmp_p = ICMPv6EchoRequest(data='A'*30)
	packet = ipv6_p/icmp_p
	send(packet,verbose=0)
	time.sleep(1.5)
	#ff02::2 -- for routers but not hosts	
	ipv6_p = IPv6(dst='ff02::2')
	icmp_p = ICMPv6ND_RS()
	packet = ipv6_p/icmp_p
	send(packet,verbose=0)
	time.sleep(1.5)
	file1 = open('hosts_scanner.txt','r')
	lines = file1.readlines()
	file1.close()
	for item in lines:
		hosts.append(item.strip())

def Port_Scanner_IPv6_TCP(host,porttcp):
	ip_p = IPv6(dst=host)
	tcp_p = TCP(dport=porttcp)
	packet = ip_p/tcp_p
	resp,non_resp = sr(packet,verbose=0,timeout=0.5)
	if resp:
		for sent,recv in resp :
			if recv.haslayer(TCP):
				if recv[TCP].flags == 18:
					packet_graceful_ter = IPv6(dst=host)/TCP(dport=sent[TCP].sport,flags=4) #Send RST packet to terminate connection gracefully
					send(packet_graceful_ter,verbose=0)
					sport = str(recv[TCP].sport)
					print'[>]Host:'+str(recv[IPv6].src)+'  Open Port:'+sport+'  Service:'+str(Vulnerable_Ports[sport])
					file1 = open('Open_Ports_results.txt','a')
					file1.write('[>]Host:'+str(recv[IPv6].src)+'  Open Port:'+sport+'  Service:'+str(Vulnerable_Ports[sport])+'\n')
					file1.close()
			else:
				pass
	
				
def Port_Scanner_IPv6_UDP(host,portudp):
	closed_ports =[]
	ip_p = IPv6(dst=host)
	udp_p = UDP(dport=portudp)
	packet = ip_p/udp_p
	resp,non_resp = sr(packet,timeout=0.5,verbose=0)
	if resp :
		for sent,recv in resp :
			if recv.haslayer(ICMP):
				closed_ports.append(portudp)
	if closed_ports == []:
		sport = str(portudp)
		print'[>]Host:'+str(host),'Opened Port:'+sport,'Service:'+str(Vulnerable_Ports[sport])
		file1 = open('Open_Ports_results.txt','a')
		file1.write('[>]Host:'+str(host)+'  Opened Port:'+sport+'  Service:'+str(Vulnerable_Ports[sport])+'\n')
		file1.close()
	
def arguments_def():
	comments = "Scapy for python3 may have a bug concerning IPv6 echo requests and replies, this also\
 affects ICMPv6ND_NA and ICMPv6ND_NS. Sometimes Scapy does not get the responses from the hosts\
 which means there might be hosts alive that Scapy does not tell you. For this reason one should\
 run the script Analyse_packets.py that will use the sniff function of scapy to capture the responses of the hosts, finally it will print the alive hosts\
 in a text file, this current script will then use that text file to append the hosts to a list and scan them. If you run this program more than once, do not forget to restart the Analyse_packets.py script. "+"\n"
	
	usage ='\n'+'This program scans the ports that are useful for a Pentration Test(To see those ports use test1.py -VulnPorts)\
 It scans the hosts of an entire internal network or a public IP address(domain).The type of scan is SYN-ACK scan(Sealth scan), or UDP depending on the port service.'+'\n'+\
 "In order to use this program, an aditional script should run at the same time in a separated terminal, the Analyse_packets.py script.\
 (type :"+"'"+sys.argv[0]+" -comments"+"'"+ "  for more information about this.)"+'\n'\
 '----------------------------------------------------------------------'+'\n'\
 '[OPTION]...[IP] ; examples :'+'\n'+sys.argv[0]+' -ipv6'+'\n'\
 +sys.argv[0]+' -ipv6 -PublicIP www.ipv6domain.com'+'\n'\
 +sys.argv[0]+' -PublicIP www.ipv6domain.com'+'\n'\
 '-----------------------------------------------------------------------'+'\n'+\
 'If desired the script Get_SysInfo.py can be run before using this program to get information about your system.\
 A Public IPv6 address can be specified at the same time, like in the examples. If both IPv6s are specified (internal\
 and external) the internal one will be scanned first.'+'\n'\
 '-----------------------------------------------------------------------'+'\n'
	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument('-ipv6',help='Scanns your internal IPv6 network. No additional arguments should be specified',action='store_true')
	parser.add_argument('-PublicIP',type=str,help='A website or its IP address(IPv6).')
	parser.add_argument('-VulnPorts',help='Prints the ports that are going to be scanned.',action='store_true')
	parser.add_argument('-comments',help='Explains you the reason why Analyse_packets.py should be run.',action='store_true')
	arguments,unknow_arguments = parser.parse_known_args()
	if unknow_arguments:
		print'[!]Unknown or unecessary arguments specified :'
		sys.exit(unknow_arguments)
	if arguments.comments:
		print comments
	if arguments.VulnPorts:
		print'Ports that are going to be scanned:'
		for item in Vulnerable_Ports:
			print'[>]'+item,':',Vulnerable_Ports[item]
	if arguments.PublicIP != None:
		if 'www' in arguments.PublicIP :
			hostname = socket.getaddrinfo(arguments.PublicIP,80,socket.AF_INET6)[2][4][0]
			print'[>]Scanning Public host',hostname
			Port_Scanner_IPv6_TCP(hostname,VulportsTCP)
			for port in VUlportsUDP:
				Port_Scanner_IPv6_UDP(hostname,port)
		if ':' in arguments.PublicIP:
			print('[>]Scanning',arguments.PublicIP)
			Port_Scanner_IPv6_TCP(arguments.PublicIP,VulportsTCP)
			for port in VUlportsUDP:
				Port_Scanner_IPv6_UDP(arguments.PublicIP,port)
	if arguments.ipv6:
		Discover_hosts()
		if hosts != []:
			print'---------------------------------------------'+'\n'+'[>]Internal hosts/routers:'
			for host in hosts :
				print'[>]Host:'+str(host)
			print'---------------------------------------------'
			for host in hosts:
				print'\n'+'[>]Scanning internal host/router:',host
				Port_Scanner_IPv6_TCP(host,VulportsTCP)
				for port in VUlportsUDP:
					Port_Scanner_IPv6_UDP(host,port)
		else:
			print'[!]No IPv6 hosts detected.'
	
def main ():
	arguments_def()
	for item in os.listdir(os.getcwd()):
		if item =='hosts_scanner.txt':
			os.remove('hosts_scanner.txt')
	print'\n'+'See Open_Ports_results.txt for results.'

main()
	
"""DO THE QUESTIONS AND COMMENTS HERE, ADD IN THE USAGE TO IGNORE THIS SENTENCE : 
"WARNING: Mac address to reach destination not found. Using broadcast."""
