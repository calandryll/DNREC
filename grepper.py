#!/usr/bin/env python3

import argparse, os, subprocess, csv
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_arguement('-f', help = 'FASTQ file to search')
parser.add_arguement('-i', help = 'Mapping file')
parser.add_arguement('-i', help = 'Output Text file')
args = parser.parse_args()

mfile = list(csv.reader(open(args.i, 'rU'), delimiter = '\t'))
ffile = args.f

for i in len(mfile):
	p1 = subprocess.Popen(['grep', mfile[i][1], ffile], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(['wc', '-l'], stdin=p1.stdout, stdout = subprocess.PIPE)
	p1.stdout.close()
	output = p2.communicate()[0]