## Sample analysis
After trial and error of trying to remove barcodes from the raw files a new approach of using the full.fasta and full.qual files will be done.

**Convert files to FASTQ**
```fish
convert_fastaqual_fastq.py -f ../originals/fasta-qual-mapping-files/062917CM515F-full.fasta -q ../originals/fasta-qual-mapping-files/062917CM515F-full.qual -o fastq
```
**Extract Barcodes**
```fish
extract_barcodes.py -f full/fastq/062917CM515F-full.fastq -m mapping.txt -o full/barcodes_1 -a -l 8
extract_barcodes.py -f full/fastq/barcodes_1/reads.fastq -o full/barcodes_2 -l 20
```
**Split Libraries**
```fish
split_libraries_fastq.py -i barcodes_2/reads.fastq -b barcodes_1/barcodes.fastq -m mapping.txt --barcode_type 8 -o split --phred_offset 33
```
>5091731  : split/seqs.fna (Sequence lengths (mean +/- std): 289.9267 +/- 8.4051)

**Pick OTUs**
```fish
pick_open_reference_otus.py -i split/seqs.fna -o otus
```
**Convert biom to table for Sourcetracker**
```fish
biom convert -i otus/otu_table_mc2_w_tax_no_pynast_failures.biom -o nonfiltered.txt --to-tsv
```
**Run Sourcetracker**
```fish
R --slave --vanilla --args -i nonfiltered.txt -m mapping.txt -o sourcetracker < $SOURCETRACKER_PATH/sourcetracker_for_qiime.r
```

## Analysis for the DADA2 pipeline
```fish
extract_barcodes.py -f Sam1-55_S30_L002_R1_001.fastq -c barcode_single_end -l 8 -o barcode_fw -a -m mapping.txt 
extract_barcodes.py -f barcode_fw/reads.fastq -c barcode_single_end -l 20 -o barcode_fw2
mv barcode_fw2/reads.fastq barcode_fw2/cleaned_R1.fastq
extract_barcodes.py -f Sam1-55_S30_L002_R2_001.fastq -c barcode_single_end -l 8 -o barcode_rw -a -m mapping.txt
extract_barcodes.py -f barcode_rw/reads.fastq -c barcode_single_end -l 20 -o barcode_rw2
mv barcode_rw2/reads.fastq barcode_rw2/cleaned_R2.fastq
split_libraries_fastq.py -i barcode_fw2/cleaned_R1.fastq -b barcode_fw/barcodes.fastq -m mapping.txt --barcode_type hamming_8 -o split_fw -r 999 -n 999 -q 0 -p 0.0001
split_libraries_fastq.py -i barcode_rw2/cleaned_R2.fastq -b barcode_rw/barcodes.fastq -m mapping.txt --barcode_type hamming_8 -o split_rw -r 999 -n 999 -q 0 -p 0.0001
```