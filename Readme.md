## Sample analysis
After trial and error of trying to remove barcodes from the raw files a new approach of using the full.fasta and full.qual files will be done.

**Convert files to FASTQ**
```fish
convert_fastaqual_fastq.py -f ../originals/fasta-qual-mapping-files/062917CM515F-full.fasta -q ../originals/fasta-qual-mapping-files/062917CM515F-full.qual -o fastq
```
**Extract Barcodes**
```fish
extract_barcodes.py -f fastq/062917CM515F-full.fastq -c barcode_single_end --bc1_len 8 -o barcodes
```
**Split Libraries**
```fish
split_libraries_fastq.py -i barcodes/reads.fastq -b barcodes/barcodes.fastq -m mapping.txt --barcode_type 8 -o split --phred_offset 33
```
>5091731  : split/seqs.fna (Sequence lengths (mean +/- std): 289.9267 +/- 8.4051)

**Pick OTUs**
```fish
pick_open_reference_otus.py -i split/seqs.fna -o otus
```