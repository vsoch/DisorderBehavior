# This script will parse the Cognitive Atlas disorder output file
# with the neurosynth papers and disorder tags

# data = read.csv("/home/vanessa/Documents/Work/BRAINBEHAVIOR/disorder_decode_thresh15.v3.txt",head=TRUE,sep="\t",stringsAsFactors=FALSE)
# data = read.csv("/home/vanessa/Documents/Work/BRAINBEHAVIOR/disorder_decode_topics.txt",head=TRUE,sep="\t",stringsAsFactors=FALSE)
data = read.csv("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/output/disorder_decode.v4.txt",head=TRUE,sep="\t",stringsAsFactors=FALSE)

rownames(data) = data$Feature
data = data[,-1]

# We are just interested in pAgF, for both topic maps and disorders
# data = data[grep("pAgF",colnames(data)),]

# Read in the names of the disorders for labels
setwd("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/output")
load("CAdisorders.Rda")

# Match dso id to image
dsos = gsub("_pAgF_z_FDR_0.05|_pFgA_z_FDR_0.05|.nii.gz|X.scratch.users.vsochat.DATA.BRAINBEHAVIOR.DisorderMaps.","",colnames(data))
#dsos = gsub("_pAgF_z_FDR_0.05|_pFgA_z_FDR_0.05|.nii.gz","",colnames(data))
idx = match(dsos,disorders$ID)
labels = disorders$NAME[idx]
colnames(data) = labels

# Get rid of topic maps with NA values
# idx = which(is.na(data),arr.ind=TRUE)
# data = data[,-unique(idx[,2])]

# Try a simple clustering
disty = dist(t(data))
hc = hclust(disty)
png(filename = "../img/clusteringpAgF_3160.png",width = 600, height = 480, units = "px", pointsize = 12)
plot(hc,main="Cognitive Atlas Disorder Clustering Based on with NSynth Terms",cex=1,xlab="",xaxt="n",sub="")
dev.off()

# Get rid of noise maps
topics_meta = read.csv("/home/vanessa/Documents/Work/NEUROSYNTH/topicmaps/Table_S1.csv",sep="\t",stringsAsFactors=FALSE)
numbers_to_remove = topics_meta$Topic.Number[which(topics_meta$Classification %in% c("Exclude")] - 1
numbers = as.numeric(gsub("topic|_pAgF_z_FDR_0.05.nii.gz","",colnames(data)))
subset = data[,-which(numbers %in% numbers_to_remove)]
disty = dist(subset)
hc = hclust(disty)
png(filename = "clusteringpAgF_onlypsych.png",width = 600, height = 480, units = "px", pointsize = 12)
plot(hc,main="Cognitive Atlas Disorder Clustering Based on NSynth Meta Analysis Maps, only psych maps , pAgF",cex=1,xlab="",xaxt="n",sub="")
dev.off()


# Now try building a som
library("kohonen")
library("RColorBrewer")
som = som(as.matrix(t(data)), grid = somgrid(3, 3, "hexagonal"))

# Now prepare labels
classes = unique(som$unit.classif)
prettyLabels = array(dim=9)
for (c in 1:length(classes)){
  group = rownames(som$data)[which(som$unit.classif == classes[c])]
  prettyLabels[classes[c]] = paste(group,collapse="\n")
}
#colorscale = rainbow(10)
#colorscale = brewer.pal(9,"YlOrRd")
#colorscale = colorRampPalette(brewer.pal(8,"YlOrRd"))(100)

# Here is the range of values
test = seq(from=min(data),to =max(data), by = ((max(data) - min(data))/(ncol(data) - 1)))

# Now assign colors to the values
color = colorscale[as.numeric(cut(test,breaks = 10))]

plot(som$grid$pts,main="Cognitive Atlas Disorders --> NSynth Meta Analysis Maps SOM, Gr 15 Unique PMID",col="orange",pch=19,xlab="Nodes",ylab="Nodes",xaxt="n",yaxt="n",cex=6)
text(som$grid$pts,prettyLabels,cex=.6)

# Let's also plot based on the search terms, so we can find ones that should be eliminated
terms = read.csv("stemmed_filtered_disorders.txt",head=FALSE,sep="\t",stringsAsFactors=FALSE)
colnames(terms) = c("ID","SEARCH")
idx = match(dsos,terms$ID)
searchlabel = terms$SEARCH[idx]

prettySearchLabels = array(dim=100)
for (c in 1:length(classes)){
  group = searchlabel[which(som$unit.classif == classes[c])]
  prettySearchLabels[classes[c]] = paste(group,collapse="\n")
}

plot(som$grid$pts,main="Cognitive Atlas Disorders --> NSynth Meta Analysis Maps SOM",col=sample(colours(),1),pch=19,xlab="Nodes",ylab="Nodes",cex=6)
text(som$grid$pts,prettySearchLabels,cex=.6)
