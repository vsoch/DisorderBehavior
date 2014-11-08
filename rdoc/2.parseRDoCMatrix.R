# This script will parse the Cognitive Atlas disorder output file
# with the neurosynth papers and disorder tags

setwd("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/data")
rdoc = read.csv(file="RDoCMatrix.tab",head=TRUE,sep="\t",stringsAsFactors=FALSE)
save(rdoc,file="rdoc.Rda")

# Find regular expressions that are false positives
for (c in 1:ncol(data)){
  cat(file="false_positives.txt",colnames(data)[c],as.character(colSums(data[c])),sep="|",append=TRUE)
  cat(file="false_positives.txt","\n",append=TRUE)
}

# For each group, output list to file
outfile = "disorder_pid_groups.txt"
sink(outfile)
for (c in 1:ncol(data)){
  pmids = paste(rownames(data)[which(data[,c]==1)],collapse="\t")
  disorder = colnames(data)[c]
  string = paste(disorder,pmids,sep="\t")
  cat(file=outfile,string,"\n",append=TRUE)
}
sink()
save(rdoc,file="rdoc.2.Rda")
# Here we want to make a list of labels and search terms, one for each entity in the matrix.  We can then
# search for these terms in abstracts to try and "classify" papers into the matrix
load("rdoc.Rda")
