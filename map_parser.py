#!/usr/bin/env python3

import csv, argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action = 'version', version = '0.1')
parser.add_argument('-f', help = 'FASTQ file to search')
parser.add_argument('-o', help = 'FASTQ file to write results to')
parser.add_argument('-i', help = 'Mapping file')
args = parser.parse_args()

print('Loading %s to memory...' % (args.f))
id_file = args.i
input_file = args.f
output_file = args.o

wanted = set(line.rstrip("\n").split(None,1)[0] for line in open(id_file))
print("Found %i unique identifiers in %s" % (len(wanted), id_file))

count = 0
handle = open(output_file, "w")
for title, seq, qual in FastqGeneralIterator(open(input_file)) :
    if title.split(None,1)[0] in wanted:
        handle.write("@%s\n%s\n+\n%s\n" % (title, seq, qual))
        count += 1
handle.close()

print("Saved %i records from %s to %s" % (count, input_file, output_file))
if count < len(wanted):
    print("Warning %i IDs not found in %s" % (len(wanted)-count, input_file))