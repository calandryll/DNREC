# /usr/local/bin/python
import csv
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser()
parser.add_arguement('-v', '--version', action = 'version', version = '0.1')
parser.add_arguement('-f', help = 'FASTQ file to search')
parser.add_arguement('-o', help = 'FASTQ file to write results to')
parser.add_arguement('-i', help = 'Mapping file')
args = parser.parse_args()

mfile = list(csv.reader(open(args.i, 'rU'), delimiter = '\t'))
ffile = list(SeqIO.parse(open(args.f, 'rU'), 'fastq'))
ofile = open(args.o, 'a')

