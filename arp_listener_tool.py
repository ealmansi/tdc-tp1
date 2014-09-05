#!/usr/bin/env python

import logging; logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all

def monitor_callback(pkt):
  pass

def main():
  scapy.all.sniff(prn=monitor_callback, filter = "arp", store = 0)

if __name__ == '__main__':
  main()