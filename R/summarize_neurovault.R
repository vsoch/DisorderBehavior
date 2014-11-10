# summarizeNeuroVault.R

# This script will read in the images and collections meta data from NeuroVault, and summarize different fields
setwd("/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/data")

# Read in image meta data
images = read.csv(file="NeuroVaultImageMeta.tab",head=TRUE,sep="\t")
images$description = as.character(images$description)

# Read in collections meta data
collections = read.csv(file="NeuroVaultCollectionsMeta.tab",head=TRUE,sep="\t")

# Print descriptions to file - need this to figure out diseases
tmp = data.frame(descriptions = images$description, name = images$name, collection = images$collection)
write.table(tmp,file="imageDisorderLookup.csv",sep="\t",quote=FALSE,row.names=FALSE)
# We can look at the collections ID link (and paper) to determine the disease cohort!







