#!/usr/bin/env python3.6
# Shell script for combining all the different parts and pieces of Qiime
# Validation of the mapping file should occur before beginning this process

# Allow running of commandline options
import subprocess
import configparser
import argparse
import os
import logging
import time
import math

parser = argparse.ArgumentParser(description = 'Combined pipeline for processing NGS samples')
parser.add_argument('file', help = 'Location of the parameters file')
args = parser.parse_args()

logfile = os.path.splitext(args.file)[0] + time.strftime('%Y-%m-%d-%H%M') + '.log'
logging.basicConfig(filename = logfile, level = logging.INFO)

# Read in parameter file
config = configparser.ConfigParser()
config.read(args.file)

# Read in parameters options
locations = config['Files']
output_options = config['Output']
options = config['Options']

logging.info('Analysis began: %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))

# Run the split_libraries_fastq.py
if not os.path.isdir(output_options['split_lib']):
	logging.info('Demultiplexing and quality filtering of sequences %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))
	subprocess.run(['split_libraries_fastq.py', '-o', output_options['split_lib'], \
		'-i', locations['reads'], '-b', locations['barcodes'], \
		'-m', locations['mapping'], '-q', options['phred'], \
		'--store_qual_scores'])
	logging.info('Command run: split_libraries_fastq.py -o %s -i %s -b %s -m %s -q %s --store_qual_scores' \
		% (output_options['split_lib'], \
		locations['reads'], locations['barcodes'], \
		locations['mapping'], options['phred']))
	#logging.info('Sequence Counts:')
	#subprocess.Popen(['count_seqs.py', '-i', \
	#	output_options['split_lib'] + '/seqs.fna']).communicate()[0]
else:
	logging.info('split_libraries_fastq.py: Directory still exists, using previous run data')

# OTU Picking using open-reference
if not os.path.isdir(output_options['otus']):
	logging.info('Picking OTUs via open reference %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))
	subprocess.run(['pick_open_reference_otus.py', '-o', output_options['otus'], \
		'-i', output_options['split_lib'] + '/seqs.fna'])
	logging.info('Command run: pick_open_reference_otus.py -o %s -i %s/seqs.fna' \
		% (output_options['otus'], output_options['split_lib']))
else:
	logging.info('pick_open_reference_otus.py: Directory still exists, using previous run data')

# Run biom to get the sampling depth (Suggested to be the Min from biom)
biom = subprocess.Popen(['biom', 'summarize-table', '-i', \
	output_options['otus'] + '/otu_table_mc2_w_tax_no_pynast_failures.biom'], \
	stdout=subprocess.PIPE).communicate()[0]
logging.info('biom analysis:')
logging.info('Command run: biom summarize-table -i %s/otu_table_mc2_w_tax_no_pynast_failures.biom' \
	% (output_options['otus']))

# Get the sampling depth, which is the lowest value in counts/sample summary from biom
biom_e = biom.decode().split('\n')[6].split(': ')[1].split('.')[0].replace(',', '')

# Run Diversity Analysis
if not options['categories']:
	logging.info('Running without Categories %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))
	subprocess.run(['core_diversity_analyses.py', '-o', output_options['core_diversity'], \
	'-i', output_options['otus'] + '/otu_table_mc2_w_tax_no_pynast_failures.biom', \
	'-m', locations['mapping'], '-e', biom_e, \
	'-t', output_options['otus'] + '/rep_set.tre', '--recover_from_failure'])
	logging.info('Command run: core_diversity_analyses.py -o %s \
	-i %s/otu_table_mc2_w_tax_no_pynast_failures.biom -m %s -e %s \
	-t %s/rep_set.tre --recover_from_failure' % (output_options['core_diversity'],\
		output_options['otus'], locations['mapping'], biom_e, output_options['otus']))
else:
	logging.info('Running with Categories %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))
	subprocess.run(['core_diversity_analyses.py', '-o', output_options['core_diversity'], \
	'-i', output_options['otus'] + '/otu_table_mc2_w_tax_no_pynast_failures.biom', \
	'-m', locations['mapping'], '-e', biom_e, \
	'-t', output_options['otus'] + '/rep_set.tre', '--recover_from_failure', \
	'-c', options['categories']])
	logging.info('Command run: core_diversity_analyses.py -o %s \
	-i %s/otu_table_mc2_w_tax_no_pynast_failures.biom -m %s -e %s \
	-t %s/rep_set.tre --recover_from_failure -c %s' % (output_options['core_diversity'],\
		output_options['otus'], locations['mapping'], biom_e, output_options['otus'], options['categories']))

# Run SourceTracker Analysis
# A column for source and sink must be in the map.txt file
logging.info('Determining Sources of bacteria %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))
subprocess.run(['filter_otus_from_otu_table.py', '-i', \
	output_options['otus'] + '/otu_table_mc2_w_tax_no_pynast_failures.biom', \
	'-o', output_options['otus'] + '/filtered_otu_table.biom', '-s', options['rare']])
subprocess.run(['biom', 'convert', '-i', output_options['otus'] + '/filtered_otu_table.biom', \
	'-o', output_options['otus'] + '/filtered_otu_table.txt', '--to-tsv'])
subprocess.run(['Rscript', locations['software'] + '/sourcetracker-1.0.0-release/sourcetracker_for_qiime.r', \
	'-i', output_options['otus'] + '/filtered_otu_table.txt', '-m', locations['mapping'], '-o', output_options['sourcetracker']])

logging.info('Analysis ended: %s' % (time.strftime('%Y-%d-%m %H:%M:%S')))