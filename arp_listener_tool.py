#!/usr/bin/env python

import logging; logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all;
import math;

# ejercicio 1

def ej1():
  scapy.all.sniff(prn=monitor_callback_ej1, filter = "arp")

def monitor_callback_ej1(pkt):
  if scapy.all.ARP in pkt:
    pkt[scapy.all.ARP].show()

# ejercicio 2

s_dst = []
s_src = []

def ej2():
  global s_dst
  global s_src
  scapy.all.sniff(prn=monitor_callback_ej2, filter = "arp", timeout=1800, count=500)
  print "s_dst"
  compute_source_indicators(s_dst)
  print "s_src"
  compute_source_indicators(s_src)

def monitor_callback_ej2(pkt):
  global s_dst
  global s_src
  if scapy.all.ARP in pkt and pkt[scapy.all.ARP].op == 1: # who-has
    s_dst.append(pkt[scapy.all.ARP].pdst)
    s_src.append(pkt[scapy.all.ARP].psrc)
    print "Paquetes ARP who-has recibidos: %d" % len(s_dst)

def compute_source_indicators(source):
  source_hist = compute_histogram(source)
  source_info = compute_information(source_hist, len(source))
  source_entropy = compute_entropy(source_hist, source_info, len(source))
  print "  hist ", source_hist
  print "  info ", source_info
  print "  entropy ", source_entropy
  print ""

def compute_histogram(ips):
  hist = {}
  for ip in ips: hist[ip] = hist.get(ip, 0) + 1
  return hist

def compute_information(hist, total):
  info = {}
  for ip in hist: info[ip] = math.log(total, 2) - math.log(hist[ip], 2)
  return info

def compute_entropy(hist, info, total):
  entropy = 0
  for ip in hist: entropy = entropy + float(hist[ip]) / total * info[ip]
  return entropy

if __name__ == '__main__':
  ej1()
  #ej2()