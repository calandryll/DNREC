import sys
from Bio import SeqIO

def sequence_cleaner(fasta_file):
    # Create our hash table to add the sequences
    sequences={}

    # Using the Biopython fasta parse we can read our fasta input
    for seq_record in SeqIO.parse(fasta_file, "fastq"):
        # Take the current sequence
        sequence = str(seq_record.seq).upper()
        if sequence not in sequences:
            sequences[sequence] = seq_record.seq

    # Write the clean sequences

    # Create a file in the same directory where you ran this script
    with open("clear_" + fasta_file, "w+") as output_file:
        # Just read the hash table and write on the file as a fasta format
        for sequence in sequences:
            output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")

    print("CLEAN!!!\nPlease check clear_" + fasta_file)


userParameters = sys.argv[1:]

sequence_cleaner(userParameters[0])
