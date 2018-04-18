# Pythonsec
Learning Python as applicable for use in security testing.
The original script I worked upon (and hopefully improved) was found here http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python

The changes found here are based on helpful comments from the above page and also my own changes to the original script.

There are also a bunch of scripts discovered elsewhere on the web for studying and modifying in order to see which method works best and in which situation. During my investigation into this, I found that there are several methods which can be used for port scanning

Things to be done:
- Scanning multiple hosts.
- Threading.
- Investigate which method for scanning is better in a given scenario.
- Ensure the script works on Python 3.6.5

remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
startPort = int(raw_input("Enter the start port to scan: "))
endPort = int(raw_input("Enter the end port to scan: "))

**** OR ****

import threading
from queue import Queue
import time, socket

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()

target = 'hackthissite.org'
#ip = socket.gethostbyname(target)

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target,port))
        with print_lock:
            print('port',port)
        con.close()
    except:
        pass


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()


# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(30):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()


start = time.time()

# 100 jobs assigned.
for worker in range(1,100):
    q.put(worker)

# wait until the thread terminates.
q.join()

-----------------------
# Another imperfect example from https://stackoverflow.com/questions/26174743/making-a-fast-port-scanner
import socket
ip = "External IP"
s = socket.socket(2, 1) #socket.AF_INET, socket.SOCK_STREAM

def porttry(ip, port):
    try:
        s.connect((ip, port))
        return True
    except:
        return None

for port in range(0, 10000):
    value = porttry(ip, port)
    if value == None:
        print("Port not opened on %d" % port)
    else:
        print("Port opened on %d" % port)
        break
raw_input()
---------------------
# This script runs on Python 3
import socket, threading


def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''



def scan_ports(host_ip, delay):

    threads = []        # To run TCP_connect concurrently
    output = {}         # For printing purposes

    # Spawning threads to scan ports
    for i in range(10000):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    # Starting threads
    for i in range(10000):
        threads[i].start()

    # Locking the script until all threads complete
    for i in range(10000):
        threads[i].join()

    # Printing listening ports from small to large
    for i in range(10000):
        if output[i] == 'Listening':
            print(str(i) + ': ' + output[i])



def main():
    host_ip = input("Enter host IP: ")
    delay = int(input("How many seconds the socket is going to wait until timeout: "))   
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()
--------------------------------------------------
#This is a quick and simple port scanner, it scans 100000 ports in 180 sec.
import threading
import socket

target = 'pythonprogramming.net'
#ip = socket.gethostbyname(target)

def portscan(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)# 

    try:
        con = s.connect((target,port))

        print('Port :',port,"is open.")

        con.close()
    except: 
        pass
r = 1 
for x in range(1,100): 

    t = threading.Thread(target=portscan,kwargs={'port':r}) 

    r += 1     
    t.start() 
--------------------------------------------------
# From http://www.coderholic.com/python-port-scanner/
#!/usr/bin/env python
from socket import * 

if __name__ == '__main__':
    target = raw_input('Enter host to scan: ')
    targetIP = gethostbyname(target)
    print 'Starting scan on host ', targetIP

    #scan reserved ports
    for i in range(20, 1025):
        s = socket(AF_INET, SOCK_STREAM)

        result = s.connect_ex((targetIP, i))

        if(result == 0) :
            print 'Port %d: OPEN' % (i,)
        s.close()
--------------------------------------------------
# 
#-*-coding:utf8;-*-
#qpy:3
#qpy:console

import socket
import os

# This is used to set a default timeout on socket
# objects.
DEFAULT_TIMEOUT = 0.5

# This is used for checking if a call to socket.connect_ex
# was successful.
SUCCESS = 0

def check_port(*host_port, timeout=DEFAULT_TIMEOUT):
    ''' Try to connect to a specified host on a specified port.
    If the connection takes longer then the TIMEOUT we set we assume
    the host is down. If the connection is a success we can safely assume
    the host is up and listing on port x. If the connection fails for any
    other reason we assume the host is down and the port is closed.'''

    # Create and configure the socket.
    sock = socket.socket()
    sock.settimeout(timeout)

    # the SO_REUSEADDR flag tells the kernel to reuse a local 
    # socket in TIME_WAIT state, without waiting for its natural
    # timeout to expire.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Like connect(address), but return an error indicator instead
    # of raising an exception for errors returned by the C-level connect() 
    # call (other problems, such as “host not found,” can still raise exceptions). 
    # The error indicator is 0 if the operation succeeded, otherwise the value of 
    # the errnovariable. This is useful to support, for example, asynchronous connects.
    connected = sock.connect_ex(host_port) is SUCCESS

    # Mark the socket closed. 
    # The underlying system resource (e.g. a file descriptor)
    # is also closed when all file objects from makefile() are closed.
    # Once that happens, all future operations on the socket object will fail. 
    # The remote end will receive no more data (after queued data is flushed).
    sock.close()

    # return True if port is open or False if port is closed.
    return connected


con = check_port('www.google.com', 83)
print(con)
--------------------------------------------------
NOTES from commenters:
--------------------------------------------------
Consider setting a timeout instead of a for loop by using socket.setdefaulttimeout(timeout).
socket.setdefaulttimeout(0.5) This will make the program faster!
-----------
***This is intended to be a learning resource for securing networks so please be responsible***
***It's also very much a work in progress.
