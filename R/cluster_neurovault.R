setwd("/home/vanessa/Documents/Work/BRAINBEHAVIOR")

# First let's summarize the voxel count data
features = read.csv("regional_features.tsv",sep="\t",head=TRUE)

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
matrix = read.csv("neurovault_z1pt96.tsv",sep="\t",head=TRUE)
matrix = t(matrix)

# Here we have images in rows, calculate distance matrix
disty = dist(matrix)

# Fit MDS model for 2 dimensions
fit = cmdscale(disty,eig=TRUE, k=2) 

# plot solution
x = fit$points[,1]
y = fit$points[,2]
labels = gsub("X.home.vanessa.Documents.Work.BRAINBEHAVIOR.mrs.|.nii.gz","",rownames(matrix))
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",main="MDS of NeuroVault")
text(x, y, labels = labels, cex=.7) 
