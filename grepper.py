#!/usr/bin/env python3

import argparse, os, subprocess, csv

parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'FASTQ file to search')
parser.add_argument('-i', help = 'Mapping file')
parser.add_argument('-o', help = 'Output Text file')
args = parser.parse_args()

handle = open(args.i, 'rU')
mfile = list(csv.reader(handle, delimiter = '\t'))
ffile = args.f
ofile = open(args.o, 'a')

for i in range(len(mfile)):
	print('Processing %s' % mfile[i][0])
	p1 = subprocess.Popen(['grep', '^' + mfile[i][1], ffile], stdout = subprocess.PIPE)
	p2 = subprocess.Popen(['wc', '-l'], stdin = p1.stdout, stdout = subprocess.PIPE)
	p1.stdout.close()
	output = p2.communicate()[0]
	ofile.write('%s\t%s\n' % (mfile[i][0], int(output)))

ofile.close()
