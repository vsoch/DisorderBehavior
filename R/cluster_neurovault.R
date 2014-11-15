setwd("/home/vanessa/Documents/Work/BRAINBEHAVIOR")

# First let's summarize the voxel count data
features = read.csv("regional_features_nothresh.tsv",sep="\t",head=TRUE)

# Get rid of empty regions
features = features[,-which(colSums(features)==0)]

# Get rid of X column
features = features[,-which(colnames(features)=="X")]

# Get full counts for each region
voxel_sums = colSums(features)
voxel_sums = log(voxel_sums)
voxel_sums = sort(voxel_sums)

# Let's color based on the brain atlas
unique_atlas =  c("JHU.ICBM","Thalamus","HarvardOxford.sub","HarvardOxford.cort","Cerebellum.MNIflirt","striatum.structural")
colors = rainbow(length(unique_atlas))
names(colors) = unique_atlas
color_labels = array(length(voxel_sums))
for (atlas in unique_atlas){
  color_labels[grep(atlas,names(voxel_sums))] = colors[[atlas]]
}

# Now make a barplot to see the regional counts
outimg = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/img/regional_voxel_counts.png"
png(filename = outimg,width = 900, height = 480, units = "px", pointsize = 12)
bp = barplot(sort(voxel_sums),main="Summed Voxel Counts for Different Atlas Regions",ylab="log transformed counts",xlab="regions",las=2,col=color_labels)
legend(10,13, unique_atlas,lty=c(1,1),lwd=c(2.5,2),col=colors)
dev.off()

# Now let's try clustering based on the regional counts
disty = dist(features)
hc = hclust(disty)
outimg = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/img/neurovault_region_clustering.png"
png(filename = outimg,width = 900, height = 480, units = "px", pointsize = 12)
plot(hc,main="Clustering of NeuroVault Images by Regional Voxel Counts",xlab="",sub="")
dev.off()

# And finally, a som
library("kohonen")
library("RColorBrewer")
som = som(as.matrix(features), grid = somgrid(10, 10, "hexagonal"))
rownames(som$data) = seq(1,length(som$unit.classif))

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

outimg = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/img/neurovault_region_som.png"
png(filename = outimg,width = 900, height = 480, units = "px", pointsize = 12)
plot(som$grid$pts,main="NeuroVault Disorder SOM From Regional Features",col="orange",pch=19,xlab="Nodes",ylab="Nodes",xaxt="n",yaxt="n",cex=6)
text(som$grid$pts,prettyLabels,cex=.6)
dev.off()

#TODO: Dimensionality reduction on actual image matrix
#TODO: more interesting labels for images!
# First let's do dimensionality reduction of the Z score, thresholded > 1.96 images
matrix = read.csv("neurovault_z_nothresh.tsv",sep="\t",head=TRUE)
matrix = t(matrix)

# let's calculate a similarity score to our SOM matrix
load ("/home/vanessa/Documents/Work/BRAINBEHAVIOR/brainMap.Rda")

# For each image in neurovault, calculate the pearson correlation to each node
nvsim = array(dim=c(nrow(matrix),nrow(brainMap$som$codes)))
for (nv in 1:nrow(nvsim)){
  cat(nv,"of",nrow(nvsim),"\n")
  nvimage = matrix[nv,]
  for (bm in 1:ncol(nvsim)) {
    node = brainMap$som$codes[bm,]
    nvsim[nv,bm] = cor(nvimage,node,method="pearson")
  }
}

library("RColorBrewer")
rbPal <- colorRampPalette(brewer.pal(8,"YlOrRd"))

# Set NA to zero
nvsim[is.na(nvsim)] = 0
# Scale to max and min neurovault values
maxy = max(nvsim)
miny = min(nvsim)

# Now let's plot the som for an image:
for (nv in 1:nrow(nvsim)){
  # Here are 506 match scores
  dat = nvsim[nv,]
  dat = c(miny,as.numeric(dat),maxy)
  color = rbPal(10)[as.numeric(cut(dat,breaks=10))]
  color = color[-c(1,508)]
  png(file=paste("img/som/",rownames(nvsim)[nv],".png",sep=""),width=14,height=14,units="in",res=300) 
 plot(brainMap$som$grid$pts,main=paste("Brainmap",rownames(nvsim)[nv]),col=color,xlab="Meta Brain Map Nodes",ylab="Meta Brain Map Nodes",pch=15,cex=8)
  text(brainMap$som$grid$pts,brainMap$labels,cex=.5)   
  dev.off()
}

# MATCHING TO NEUROSYNTH TOPIC MAPS
# We removed / filtered out the NA maps.
matrix = read.csv("nv2nsy_pearson.tsv",sep="\t",head=TRUE)
matrix[is.na(matrix)] = 0
matrix = matrix[,-which(colSums(matrix)==0)]

source("/home/vanessa/Documents/Dropbox/Code/R/DNS/functions_quest_analysis.R")
library(qgraph)
library(psych)
library(pheatmap)
library(nFactors)
library(Hmisc)

# Simple heatmap
png(file="../../img/nv2topics.png",width=14,height=14,units="in",res=300) 
heatmap(as.matrix(matrix),main="NeuroVault Imgages to NeuroSynth Topics")
dev.off()

# Better heatmap
colnames(matrix) = gsub("X.home.vanessa.Documents.Work.BRAINBEHAVIOR.mrs.","",colnames(matrix))
png(file="../../img/nv2topicsHeatmap.png",width=20,height=10,units="in",res=300) 
pheatmap(matrix)
dev.off()

# Get rid of column labels
colnames(matrix) = NA
png(file="../../img/nv2topicsHeatmapDetail.png",width=20,height=10,units="in",res=300) 
pheatmap(matrix)
dev.off()

# Now, for one image, show 
library("RColorBrewer")
rbPal <- colorRampPalette(brewer.pal(8,"YlOrRd"))

# Set NA to zero
nvsim[is.na(nvsim)] = 0
# Scale to max and min neurovault values
maxy = max(nvsim)
miny = min(nvsim)

# Now let's plot the som for an image:
for (nv in 1:nrow(nvsim)){
  # Here are 506 match scores
  dat = nvsim[nv,]
  dat = c(miny,as.numeric(dat),maxy)
  color = rbPal(10)[as.numeric(cut(dat,breaks=10))]
  color = color[-c(1,508)]
  png(file=paste("img/som/",rownames(nvsim)[nv],".png",sep=""),width=14,height=14,units="in",res=300) 
 plot(brainMap$som$grid$pts,main=paste("Brainmap",rownames(nvsim)[nv]),col=color,xlab="Meta Brain Map Nodes",ylab="Meta Brain Map Nodes",pch=15,cex=8)
  text(brainMap$som$grid$pts,brainMap$labels,cex=.5)   
  dev.off()
}

# NEXT: I want strategy to see ONE map. How does it compare?
