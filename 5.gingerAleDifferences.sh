#!/bin/sh

# Create map of significantly different voxels in two images
args=("$@")

if [ $# -ne 2 ]; then
  echo "Please supply two input arguments: two statistical maps to compare!"
fi

# Read in image paths from command line
image1=${args[0]}
image2=${args[1]}
image1="/home/vanessa/Desktop/tmp/dso_1094_pAgF_z_FDR_0.05.nii.gz"
image2="/home/vanessa/Desktop/tmp/dso_1206_pAgF_z_FDR_0.05.nii.gz"

# Get absolute paths of images
image1=`readlink -e $image1`
image2=`readlink -e $image1`

# Path to save cluster images
DIR=$(dirname ${image1})
base1=$(basename ${image1})
base2=$(basename ${image2})

# Get absolute path of GingerAle
ALE=`readlink -e inc/GingerALE.jar`

# Create a "cluster image" for each input image that is required in the analysis step
# We will suppress output
echo "Creating cluster image for " $base1
java -cp $ALE org.brainmap.meta.getClustersOnly $image1 -out=$DIR/cluster_$base1g >/dev/null
echo "Creating cluster image for " $base2
java -cp $ALE org.brainmap.meta.getClustersOnly $image2 -out=$DIR/cluster_$base2 >/dev/null
