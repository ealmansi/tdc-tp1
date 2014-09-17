#!/usr/bin/env python

import sys;
import time;
import math;
import matplotlib.pyplot as plt;

def main():
  s_src, s_dst = read_data()
  hist, info, entropy = compute_source_indicators(s_src)
  print_indicators('s_src', hist, info, entropy)
  plot_histogram('s_src', hist)
  hist, info, entropy = compute_source_indicators(s_dst)
  print_indicators('s_dst', hist, info, entropy)
  plot_histogram('s_dst', hist)

def read_data():
  s_src, s_dst = [], []
  for line in sys.stdin:
    pieces = line.split(",")
    ip_src, ip_dst = pieces[0].strip(), pieces[1].strip()
    s_src.append(ip_src)
    s_dst.append(ip_dst)
  return s_src, s_dst

def compute_source_indicators(source):
  hist = compute_histogram(source)
  info = compute_information(hist, len(source))
  entropy = compute_entropy(hist, info, len(source))
  return hist, info, entropy
  
def print_indicators(source, hist, info, entropy):
  print source
  print "  hist ", hist
  print "  info ", info
  print "  entropy ", entropy
  print ""

def plot_histogram(source, hist):
  hist = { k:v for (k,v) in hist.iteritems() if 2 < v }
  x, y = [2 * i for i in range(len(hist))], hist.values()
  labels = hist.keys()
  f = plt.figure(source, [12, 6])
  plt.xlim([-2, x[-1] + 2])
  plt.bar(x, y, align='center')
  plt.xticks(x, labels, size='small')
  plt.title(source)
  plt.xlabel("IP")
  plt.ylabel("Cantidad de paquetes")
  f.savefig('imgs/{source}.png'.format(source=source))

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
  main()