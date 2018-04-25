# Original code from http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
#!/usr/bin/env python

# modules
import threading, socket, subprocess, sys, time
from queue import queue
from datetime import datetime

subprocess.call('clear', shell=True)

# Enter target host and port range
remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
startPort = int(raw_input("Enter the start port to scan: "))
endPort = int(raw_input("Enter the end port to scan: "))

# Banner displaying which host is being scanned
print ("-" * 60)
print ("Please wait, scanning remote host...", remoteServerIP)
localtime = time.asctime(time.localtime())
print ("Scan started at: ", localtime)
print ("-" * 60)

# Check what time the scan started
t1 = datetime.now()

# Error handling
try:
    for port in range(startPort,endPort):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
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

# Checking the time again
t2 = datetime.now()

# Calculates the difference in time, to see how long it took to run the script
total =  t2 - t1
print ("-" * 60)

# Display scan time taken
print ("Scanning Completed in: ", total)
