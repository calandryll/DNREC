#!/usr/bin/env python3

import argparse, os, subprocess, csv
from Bio.Seq import Seq

parser = argparse.ArgumentParser()
parser.add_argument('-f', help = 'FASTQ file to search')
parser.add_argument('-i', help = 'Mapping file')
#parser.add_argument('-o', help = 'Output Text file')
args = parser.parse_args()

handle = open(args.i, 'rU')
mfile = list(csv.reader(handle, delimiter = '\t'))
ffile = args.f
#ofile = open(args.o, 'a')

for i in range(len(mfile)):
	if i == 0:
		print('Processing')
	else:
		print('Processing %s' % mfile[i][0])
		p1 = subprocess.Popen(['grep', '-B', '1', '^' + mfile[i][1], ffile], stdout = subprocess.PIPE)
		#p2 = subprocess.Popen(['wc', '-l'], stdin = p1.stdout, stdout = subprocess.PIPE)
		p2 = subprocess.Popen(['grep', '@D00420'], stdin = p1.stdout, stdout = subprocess.PIPE)
		p1.stdout.close()
		output = str(p2.communicate()[0]).split('\\n')
		#rc = mfile[i][1].reverse_complement()
		#print(rc)
		#p1 = 
		outfile = mfile[i][0] + '.txt'
		ofile = open(outfile, 'a')
		for l in range(len(output)):
			ofile.write('%s\n' % (output[l]))

ofile.close()
