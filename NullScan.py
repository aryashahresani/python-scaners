#!/usr/bin/env python

#Importing the logging module
import logging

#This will suppress all messages that have a lower level of seriousness than error messages.
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

#Importing Scapy and handling the ImportError exception
try:
    from scapy.all import *

except ImportError:
    print("Scapy package for Python is not installed on your system.")
    print("Get it from https://pypi.python.org/pypi/scapy and try again.")
    sys.exit()

#Defining the destination name/IP
#target = '172.16.1.2'
target = '192.168.10.1'

#Performing the scan
ans, unans = sr(IP(dst = target) / TCP(sport = RandShort(), dport = [111, 135, 22], flags = 0, seq = 0), timeout = 5)

#The results based on closed ports
for sent, received in ans:
	if received.haslayer(TCP) and str(received[TCP].flags) == "20":
		print(str(sent[TCP].dport) + " is closed!")
	elif received.haslayer(ICMP) and str(received[ICMP].type) == "3":
		print(str(sent[TCP].dport) + " is filtered!")

#Handling unanswered packets
for sent in unans:
	print(str(sent[TCP].dport) + " is open/filtered!")

'''
An attacker uses a TCP NULL scan to determine if ports are closed on the target machine. This scan type is accomplished by sending TCP segments with no flags in the packet header, generating packets that are illegal based on RFC 793. The RFC 793 expected behavior is that any TCP segment with an out-of-state Flag sent to an open port is discarded, whereas segments with out-of-state flags sent to closed ports should be handled with a RST in response. This behavior should allow an attacker to scan for closed ports by sending certain types of rule-breaking packets (out of sync or disallowed by the TCB) and detect closed ports via RST packets.

Many operating systems, however, do not implement RFC 793 exactly and for this reason NULL scans do not work as expected against these devices. Some operating systems, like Microsoft Windows, send a RST packet in response to any out-of-sync (or malformed) TCP segments received by a listening socket (rather than dropping the packet via RFC 793), thus preventing an attacker from distinguishing between open and closed ports.

Source: https://capec.mitre.org/data/definitions/304.html
'''

