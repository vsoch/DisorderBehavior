# We will use fsl to read images
library("fslr")
options(fsl.path="/usr/share/fsl/4.1")

# Visualize images
# Here is our standard space image
standard = file.path( getOption("fsl.path"), "data", "standard", "MNI152_T1_2mm_brain.nii.gz")

# Now we have a new folder of images, with voxel size 2mm.  This means that 
# some of them will be in the correct space, some might still be off.  
# Let's try visualizing:
mrdir = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs"
mrs = list.files(mrdir,full.names=TRUE)
imgdir = "/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/img"
standard = readNIfTI(standard)  

# Save those with a good dimension
rightsize = c()
wrongsize = c()
for (m in 1:length(mrs)){
  cat("Processing",m,"of",length(mrs),"\n")
  mr = mrs[m]
  img = readNIfTI(mr)
  if (all(dim(img) == dim(standard))){
    outimg = paste(imgdir,"/",gsub(".nii","",gsub(".gz","",strsplit(mr,"/")[[1]][8])),".png",sep="")
    outimg = gsub("%20","",outimg)
    png(filename=outimg,width=300,height=300)
    orthographic(standard,img,zlim=c(min(standard),max(standard)),zlim.y=c(0.01,max(img)))
    dev.off()
    rightsize = c(rightsize,mr)
  } else {
    wrongsize = c(wrongsize,mr)
  }
}

