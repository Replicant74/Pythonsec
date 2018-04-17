# Original code from http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
#!/usr/bin/env python

# modules
import socket
import subprocess
import sys
import time
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

# Enter Host to scan
remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
startPort = int(raw_input("Enter the start port to scan: "))
endPort = int(raw_input("Enter the end port to scan: "))

# Print a nice banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host...", remoteServerIP
localtime = time.asctime(time.localtime())
print "Scan started at: ", localtime
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

try:
    for port in range(startPort,endPort):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print "Port {}: [+] Open".format(port)
        elif result != 0:
            print "Port {}: [-] Closed".format(port)
        sock.close()

except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()

except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

except socket.error:
    sys.exit("Couldn't connect to server")

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1
print "-" * 60

# Printing the information to screen
print 'Scanning Completed in: ', total