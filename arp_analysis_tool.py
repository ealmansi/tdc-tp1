#!/usr/bin/env python

import sys;
import time;
import math;
import os;
import re;
import argparse;
import matplotlib.pyplot as plt;
import pydot;

def main():
  args = parse_args()
  s_src, s_dst = read_data(args)
  basename = os.path.basename(args.get('datafile')).split('.')[0]
  hist, info, entropy = compute_source_indicators(s_src)
  print_indicators('s_src', hist, info, entropy)
  plot_histogram('s_src', hist, basename)
  plot_info('s_src', info, entropy, basename)
  hist, info, entropy = compute_source_indicators(s_dst)
  print_indicators('s_dst', hist, info, entropy)
  plot_histogram('s_dst', hist, basename)
  plot_info('s_dst', info, entropy, basename)
  plot_network(s_src, s_dst, basename)

def parse_args():
  parser = argparse.ArgumentParser(description='ARP packet analysis.')
  parser.add_argument('datafile', type=str,
    help = 'data file path')
  args = vars(parser.parse_args())
  return args

def read_data(args):
  s_src, s_dst = [], []
  with open(args.get('datafile')) as f:
    for line in f:
      if not re.match('^\s*#', line):
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
  print "  - hist: ", hist
  print "  - info: ", info
  print "  - entropy: ", entropy
  print ""

def plot_histogram(source, hist, basename):
  if len(hist) > 10:
    hist = { k:v for (k,v) in hist.iteritems() if 2 < v }
  x, y = [4 * i for i in range(len(hist))], hist.values()
  labels = hist.keys()
  f = plt.figure('hist_{source}'.format(source=source), [12, 12])
  plt.xlim([-2, x[-1] + 2])
  plt.bar(x, y, align='center')
  plt.xticks(x, labels, size='small', rotation='vertical')
  plt.title('Histograma: {source}'.format(source=source))
  plt.xlabel("IP")
  plt.ylabel("Cantidad de paquetes")
  f.savefig('imgs/{basename}_{source}_hist.png'.format(basename=basename, source=source))

def plot_info(source, hist, entropy, basename):
  x, y = [4 * i for i in range(len(hist))], hist.values()
  labels = hist.keys()
  f = plt.figure('info_{source}'.format(source=source), [12, 12])
  plt.xlim([-2, x[-1] + 2])
  plt.bar(x, y, align='center')
  plt.axhline(entropy, color='r')
  plt.xticks(x, labels, size='small',rotation='vertical')
  plt.title('Informacion: {source}'.format(source=source))
  plt.xlabel("IP")
  plt.ylabel("Informacion")
  f.savefig('imgs/{basename}_{source}_info.png'.format(basename=basename, source=source))

def plot_network(s_src, s_dst, basename):
  graph = pydot.Dot(graph_type='digraph')
  nodes = {}
  for ip in set(s_src + s_dst):
    pieces = ip.split('.')
    label = '.'.join(pieces[0:2]) + '\n' + '.'.join(pieces[2:4])
    nodes[ip] = pydot.Node(label)
  edges = {}
  for i in range(len(s_src)):
    if not (s_src[i], s_dst[i]) in edges:
      edges[(s_src[i], s_dst[i])] = 0
    edges[(s_src[i], s_dst[i])] += 1
  for (src_ip, dst_ip) in edges:
    if not(len(nodes) > 10) or edges[(src_ip, dst_ip)] > 2:
      graph.add_edge(pydot.Edge(nodes[src_ip], nodes[dst_ip],
        label=edges[(src_ip, dst_ip)], fontsize="8.0", color="blue"))
  graph.write_png('imgs/{basename}_red.png'.format(basename=basename))

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
