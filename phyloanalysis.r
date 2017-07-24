library(phyloseq)

# Locate OTU file as a text file
otufile = system.file("extdata", "nonfiltered.txt", package = "phyloseq")
mapfile = system.file("extdata", "mapping.txt", package = "phyloseq")
trefile = system.file("extdata", "otus/rep_set.tre", package = "phyloseq")
fas_file = system.file("extdata", "", package = "phyloseq")