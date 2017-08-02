## 07/20/2017
**Note:** Files from MRDNA as 2017_7_18_062917CM515F_fasta-qual-mapping.zip have been previously preprocessed.  And should not be used.  Raw data from the Basespace will need to be
processed before running.

~~Files were combined using the convert_fastaqual_fastq.py command, part of the QIIME package:~~ 
~~/m/s/analysis  convert_fastaqual_fastq.py -q 062917CM515F-full.qual -f 062917CM515F-full.fasta -F                                       Thu 20 Jul 2017 04:10:30 PM EDT~~ 
~~For processing further down the pipeline barcodes were extracted using extract_barcodes.py:~~ 
~~/m/s/analysis  extract_barcodes.py -f reads.fastq -l 10 -c barcode_single_end                                                           Thu 20 Jul 2017 05:09:09 PM EDT~~ 

## 7/21/2017
**Preprocessing of sample data**

/m/s/analysis  extract_barcodes.py -f Sam1-55_S30_L002_R1_001.fastq -c barcode_single_end -l 8 -o barcode_fw                    1620ms < Fri 21 Jul 2017 05:49:49 AM EDT

/m/s/analysis  extract_barcodes.py -f Sam1-55_S30_L002_R2_001.fastq -c barcode_single_end -l 8 -o barcode_rw                      4.6m < Fri 21 Jul 2017 05:55:04 AM EDT

/m/s/analysis  extract_barcodes.py -f Sam1-55_S30_L002_R1_001.fastq -r Sam1-55_S30_L002_R2_001.fastq -o barcode -c barcode_paired_end -l 8 -L 8 --rev_comp_bc2      Fri 21 Jul 2017 08:30:36 AM EDT

/m/s/analysis  join_paired_ends.py -f Sam1-55_S30_L002_R1_001.fastq -r Sam1-55_S30_L002_R2_001.fastq -o joined                    4.4m < Fri 21 Jul 2017 06:05:24 AM EDT

/m/s/analysis  join_paired_ends.py -f Sam1-55_S30_L002_R1_001.fastq -r Sam1-55_S30_L002_R2_001.fastq -o joined_seq -m SeqPrep            Fri 21 Jul 2017 06:19:45 AM EDT

SeqPrep joins 92.5% of all reads whereas fastq-join is 97.3%.  The fastq-join results will be used for further downstream analysis.

Trying data analysis using pre-joined and stripped primer and linker sequences.

/m/s/analysis  convert_fastaqual_fastq.py -f 062917CM515F-pr.fasta -q 062917CM515F-pr.qual -c fastaqual_to_fastq -o fastq       1831ms < Fri 21 Jul 2017 12:31:47 PM EDT

**Issues with trying to get it to work with later stages.  Restarting using the join_paired_ends.py and split_libraries.py**

/m/s/analysis  split_libraries.py -m mapping.txt -f fasta/combined_seqs.fna -q fasta/combined_seqs.qual -o split -b hamming_8   1511ms < Fri 21 Jul 2017 09:41:28 PM EDT

/m/s/analysis  pick_open_reference_otus.py -o otus -i split/seqs.fna                                                                     Sat 22 Jul 2017 05:40:33 AM EDT

/m/s/analysis  core_diversity_analyses.py -o core_diversity -i otus/otu_table_mc2_w_tax_no_pynast_failures.biom -m mapping.txt -e 17432 -t otus/rep_set.tre --recover_from_failure             22.5s < Sat 22 Jul 2017 07:33:11 AM EDT

/m/s/analysis  filter_otus_from_otu_table.py -i otus/otu_table_mc2_w_tax_no_pynast_failures.biom -o filtered_otus -s 7           4.69h < Sat 22 Jul 2017 12:15:12 PM EDT

/m/s/analysis  R --slave --vanilla --args -i filtered_otus.txt -m mapping.txt -o sourcetracker_filtered < $SOURCETRACKER_PATH/sourcetracker_for_qiime.r        Sat 22 Jul 2017 01:46:20 PM EDT

## 07/24/2017
**Rarefaction analysis** 

Multiple rarefactions were performed starting with 1000 and going to 20000 at 1000 steps.

multiple_rarefactions.py -i otus/otu_table_mc2_w_tax_no_pynast_failures.biom -m 1000 -x 20000 -n 10 -o rare -s 1000

alpha_diversity.py -i rare/ -o alpha_rare -t otus/rep_set.tre -m observed_species,chao1,PD_whole_tree

**McMurdie and Holmes 2014 recommend not rarefying samples.**

A general example of processing can be found [here](https://twbattaglia.gitbooks.io/introduction-to-qiime/content/processing_sequences_md.html)

pick_open_reference_otus.py -o otus -i split/seqs.fna -o pick_otus -p 16s_pickotu_param.txt -a -O 4

Running defaults for sourcetracker

R --slave --vanilla --args -i rdp/rdp_otus.txt -m mapping.txt -o sourcetracker_defaults < $SOURCETRACKER_PATH/
sourcetracker_for_qiime.r

Non rarefaction or burnin

## 07/26/2017

**Reprocessing of sequences**

It appears that R1 and R2 are in the same orientation.  Using:

/m/s/analysis  ⎇ master …  extract_barcodes.py -f Sam1-55_S30_L002_R1_001.fastq -c barcode_single_end -l 8 -o barcode_fw

/m/s/analysis  ⎇ master …  extract_barcodes.py -f Sam1-55_S30_L002_R2_001.fastq -c barcode_single_end -l 8 -o barcode_rw

barcodes.fastq were copied as Sam1-55_S30_L002_IX_001.fastq

~~For processing in Qiime (Phred >20):~~

~~split_libraries_fastq.py -i Sam1-55_S30_L002_R1_001.fastq,Sam1-55_S30_L002_R2_001.fastq -b Sam1-55_S30_L002_I1_001.fastq,Sam1-55_S30_L002_I2_001.fastq -m mapping.txt -q 19-o split --barcode_type hamming_8~~

Commands for joining paired ends:

cat Sam1-55_S30_L002_I1_001.fastq > barcodes.fastq

cat Sam1-55_S30_L002_I2_001.fastq >> barcodes.fastq

join_paired_ends.py -f Sam1-55_S30_L002_R1_001.fastq -r Sam1-55_S30_L002_R2_001.fastq -b barcodes.fastq -o joined

cp joined/fastqjoin.join.fastq joined_reads.fastq

cp joined/fastqjoin.join_barcodes.fastq barcodes.fastq

For processing in dada2:

split_libraries_fastq.py -i joined_reads.fastq -b barcodes.fastq -m mapping.txt -r 999 -n 999 -q 0 -p 0.0001 -o dada2_joined --barcode_type hamming_8

May be better to run separately for the dada2 analysis:

split_libraries_fastq.py -i Sam1-55_S30_L002_R1_001.fastq,Sam1-55_S30_L002_R2_001.fastq -b Sam1-55_S30_L002_I1_001.fastq,Sam1-55_S30_L002_I2_001.fastq -m mapping.txt -r 999 -n 999 -q 0 -p 0.0001 -o dada2 --barcode_type hamming_8

or each individually:
split_libraries_fastq.py -i Sam1-55_S30_L002_RX_001.fastq -b Sam1-55_S30_L002_IX_001.fastq -m mapping.txt -r 999 -n 999 -q 0 -p 0.0001 -o dada2_rX --barcode_type hamming_8 --store_demultiplexed_fastq

For processing via Qiime:

split_libraries_fastq.py -i joined_reads.fastq -b barcodes.fastq -m mapping.txt -q 19 -o split --barcode_type hamming_8

and

split_libraries_fastq.py -i Sam1-55_S30_L002_R1_001.fastq,Sam1-55_S30_L002_R2_001.fastq -b Sam1-55_S30_L002_I1_001.fastq,Sam1-55_S30_L002_I2_001.fastq -m mapping.txt -q 19 -o split2 --barcode_type hamming_8

and

split_libraries_fastq.py -i barcodes/barcode_fw/reads.fastq,barcodes/barcode_rw/reads.fastq -b barcodes/barcode_fw/barcodes.fastq,barcodes/barcode_rw/barcodes.fastq -m mapping.txt -q 19 -o split3 --barcode_type hamming_8

split_libraries_fastq.py -i Sam1-55_S30_L002_R1_001.fastq,Sam1-55_S30_L002_R2_001.fastq -b Sam1-55_S30_L002_I1_001.fastq,Sam1-55_S30_L002_I2_001.fastq -m mapping.txt -q 19 -o split_fw --barcode_type hamming_8 --store_demultiplexed_fastq

split_libraries_fastq.py -i Sam1-55_S30_L002_R1_001.fastq,Sam1-55_S30_L002_R2_001.fastq -b Sam1-55_S30_L002_I1_001.fastq,Sam1-55_S30_L002_I2_001.fastq -m mapping.txt -q 19 -o split_fw --barcode_type hamming_8 --store_demultiplexed_fastq --rev_comp_barcode

## 07/27/2017
extract_barcodes.py -f Sam1-55_S30_L002_R1_001.fastq -l 8 -c barcode_single_end -o barcodes/barcodes_fw -m mapping.txt
extract_barcodes.py -f reverse_reads.fastq -l 8 -c barcode_single_end -o barcodes/barcodes_rw -m mapping.txt -a --rev_comp_bc1

convert_fastaqual_fastq.py -f ../originals/fasta-qual-mapping-files/062917CM515F-full.fasta -q ../originals/fa
sta-qual-mapping-files/062917CM515F-full.qual -o fastq

## 08/02/2017
sourcetracker2 gibbs -i full/nonfiltered.txt -m short_mapping.txt -o full/sourcetracker2 --jobs 4 --source_rarefaction_depth 30000 --sink_rarefaction_depth 30000
sourcetracker2 gibbs -i full/nonfiltered.txt -m short_mapping.txt -o full/sourcetracker3 --jobs 4
sourcetracker2 gibbs -i full/nonfiltered.txt -m short_mapping.txt -o full/sourcetracker4 --jobs 4 --source_rarefaction_depth 0 --sink_rarefaction_depth 0