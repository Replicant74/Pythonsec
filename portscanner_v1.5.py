# Original code from http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
#!/usr/bin/env python

# modules
import threading
import socket
import subprocess
import sys
import time
import scapy
from queue import Queue
from datetime import datetime
from logging import getLogger, ERROR
getLogger("scapy.runtime") .setLevel (ERROR)
from scapy.all import *

subprocess.call('clear', shell=True)

# print_lock = threading.Lock() - WIP, threading not implemented yet.

# Enter target host and port range
target    = input("Enter a remote host to scan: ")
targetIP  = socket.gethostbyname(target)
startPort = int(input("Enter the start port to scan: "))
endPort = int(input("Enter the end port to scan: "))

# Setting some values
ports = range(int(startPort), int(endPort)+1)
t1 = datetime.now()
SYNACK = 0x12
RSTACK = 0x14

# Banner displaying which host is being scanned
print ("-" * 60)
print ("Please wait, scanning remote host...", targetIP)
localtime = time.asctime(time.localtime())
print ("Scan started at: ", localtime)
def checkhost(ip):
    conf.verb = 0
    try:
        ping = sr1(IP(dst = ip)/ICMP())
        print ("\n[*] Target is up, beginning scan...") #this text isn't displayed - why?
    except Exception:
        print ("\n[!] Couldn't resolve target")
        sys.exit("Exiting...")
print ("-" * 60)

def scanport(port):
        startPort = RandShort() # scapy func that generates a small random nr to use as a source port.
        conf.verb = 0 # prevents output from sending pkts from being printed to the screen.
        SYNACKpkt = sr1(IP(dst = target)/TCP(sport = startPort, endPort = port, flags = "S")) # Scapy func sr1() used to craft & send a SYN pkt .
        pktflags = SYNACKpkt.getlayer(TCP).flags
        if pktflags == SYNACK:
                return True
        else:
                return False
        RSTpkt = IP(dst = target)/TCP(sport = startPort, endPort = port, flags = "R")
        send(RSTpkt)


# Error handling
try:
    for port in range(int(startPort), int(endPort)+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((targetIP, port))
        if result == 0:
            print ("Port {}: [+] Open".format(port))
        elif result != 0:
            print ("Port {}: [-] Closed".format(port))
        sock.close()

except KeyboardInterrupt:
    sys.exit("You pressed Ctrl+C")

except socket.gaierror:
    sys.exit("Hostname could not be resolved. Exiting")

except socket.error:
    sys.exit("Couldn't connect to server")

t2 = datetime.now()

# Calculates the difference in time, to see how long it took to run the script
total =  t2 - t1
print ("-" * 60)
print ("Scanning Completed in: ", total)
