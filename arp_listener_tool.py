#!/usr/bin/env python

import logging; logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all

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
  scapy.all.sniff(prn=monitor_callback_ej2, filter = "arp", count=10)
  s_dst_hist = compute_histogram(s_dst)
  s_src_hist = compute_histogram(s_src)
  print "s_dst_hist ", s_dst_hist
  print "s_src_hist ", s_src_hist

def monitor_callback_ej2(pkt):
  global s_dst
  global s_src
  if scapy.all.ARP in pkt and pkt[scapy.all.ARP].op == 1: # who-has
    s_dst.append(pkt[scapy.all.ARP].pdst)
    s_src.append(pkt[scapy.all.ARP].psrc)
    print "Paquetes who-has recibidos: %d" % len(s_dst)

def compute_histogram(ips):
  hist = {}
  for ip in ips: hist[ip] = hist.get(ip, 0) + 1
  for ip in hist: hist[ip] = float(hist[ip]) / len(ips)
  return hist

# main

if __name__ == '__main__':
  # ej1()
  ej2()