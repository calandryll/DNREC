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
ofile = args.o

for i in range(len(mfile)):
	print('Processing %s' % mfile[i])
	p1 = subprocess.Popen(['grep', mfile[i], ffile], stdout = subprocess.PIPE)
	p2 = subprocess.Popen(['wc', '-l'], stdin = p1.stdout, stdout = subprocess.PIPE)
	p1.stdout.close()
	output = str(p2.communicate()[0])
	ofile.write('%s\n' % (output[i]))

ofile.close()