#!/usr/bin/env python3

import argparse, os, subprocess, csv
from Bio.Seq import Seq

parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'FASTQ file to search')
parser.add_argument('-i', help = 'Mapping file')
parser.add_argument('-o', help = 'Output Text file')
args = parser.parse_args()

mfile = set(line.rstrip('\n').split(None,1)[0] for line in open(args.i))
ffile = args.f
ofile = open(args.o, 'w')
handle = list(mfile)

for i in range(len(handle)):
	print('Processing')
	#p1 = subprocess.Popen(['grep', handle[i], ffile], stdout = subprocess.PIPE)
	#p2 = subprocess.Popen(['wc', '-l'], stdin = p1.stdout, stdout = subprocess.PIPE)
	#p1.stdout.close()
	#output = p2.communicate()[0]
	#ofile.write('%s\t%s\n' % (handle[i], output))

ofile.close()