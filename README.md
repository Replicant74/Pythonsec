# Pythonsec
Learning Python as applicable for use in security testing.
Original script was found here http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
The changes found here are based on helpful comments from the above page and also my own changes to the original script.
Changes made:
- Minor changes to text strings describing what the script is doing.
- Changed to allow you to specify start port and end port.
- Changed to display a list of ports which are closed.
- Tidied up the layout and display times.

Things to be done:
- Scanning multiple hosts.
- Threading.
- Investigate which is better - 

remoteServer    = raw_input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)
startPort = int(raw_input("Enter the start port to scan: "))
endPort = int(raw_input("Enter the end port to scan: "))

**** OR ****

import threading
from queue import Queue
import time
import socket

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
