#!/usr/bin/env python3

import csv, argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action = 'version', version = '0.1')
parser.add_argument('-f', help = 'FASTQ file to search')
parser.add_argument('-o', help = 'FASTQ file to write results to')
parser.add_argument('-i', help = 'Mapping file')
args = parser.parse_args()

handle = open(args.i, 'rU')
handle2 = open(args.f, 'rU')
mfile = csv.reader(handle, delimiter = '\n')
ffile = list(SeqIO.parse(handle2, 'fastq'))
ofile = open(args.o, 'w')

print('Loading %s to memory...' % (args.f))
records = (r for r in ffile if r.id in mfile)
count = SeqIO.write(records, ofile, "fastq")

print('Saved %i of %s' % (count, len(list(ffile))))