# This script will parse the Cognitive Atlas disorder output file
# with the neurosynth papers and disorder tags

setwd("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/data")
data = read.table(file="disorder_pid_matrix.v3.txt",head=TRUE,sep="\t")
rownames(data) = data$ID
data = data[,-1]

# Find regular expressions that are false positives
for (c in 1:ncol(data)){
  cat(file="false_positives.txt",colnames(data)[c],as.character(colSums(data[c])),sep="|",append=TRUE)
  cat(file="false_positives.txt","\n",append=TRUE)
}

# We want to eliminate papers that have more than one disorder
# this creates redundancy in the database
paperseliminate = which(rowSums(data) > 1)
data = data[-paperseliminate,]

# Eliminate disorders with zero papers
data = data[,-which(colSums(data)==0)]

# What disorders are left?
setwd("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/data")
load("CAdisorders.Rda")
dsos = gsub("_pAgF_z_FDR_0.05","",colnames(data))
idx = match(dsos,disorders$ID)
labels = disorders$NAME[idx]

# Now we want to look at the number of papers we have per disorder
counts = colSums(data)
names(counts) = labels

# Visualize
png(filename = "/home/vanessa/Desktop/disorder_pmid_counts.png",width = 480, height = 480, units = "px", pointsize = 12)
barplot(sort(counts),main=paste("Number of pmids associated with each disorder"),col="orange",las=1)
dev.off()

# Threshold at 15 papers?
output = data[,as.numeric(which(counts>=15))]

# For each group, output list to file
outfile = "disorder_pid_groups_thresh15.v3.txt"
sink(outfile)
for (c in 1:ncol(output)){
  pmids = paste(rownames(output)[which(output[,c]==1)],collapse="\t")
  disorder = colnames(output)[c]
  if (pmids != "") {
    string = paste(disorder,pmids,sep="\t")
    cat(file=outfile,string,"\n",append=TRUE)
  }
}
sink()
