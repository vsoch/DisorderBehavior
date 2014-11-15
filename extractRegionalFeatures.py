#!/usr/bin/env python2

# This script will extract regional voxel counts for a set of thresholded statistical maps

import imageutils as utils
import glob
#from visualize import feature_plots

# Create a new Atlas instance to hold our atlas maps
atlas = utils.Atlas()

# Here our our images to get features for
files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs/*.nii.gz")
output_file = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/regional_features.tsv"

# STEP 1: Extract regional voxel features for all NeuroVault images ---------
df = atlas.count_voxels_in_atlas(mrs=files,output_file=output_file)

# TODO: Make plots of results (or I possibly want to just export data to database --> d3)
#output_image = "/home/vanessa/Desktop/regional_voxel_counts.png"
#feature_plots(df,output_image)



# STEP 2: Extract matrix of normalized values in 8mm voxel space for 2D visualization ----------
standard = "/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/brainbehavior/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz"
standard8mm = utils.resize_image(standard,[8,8,8])
# Get subset of images that are 3d
threed_files = utils.files_get_3d_list(files)
# Now get a matrix of image files in this space!
matrix = utils.spatial_normalize_images(threed_files,standard8mm,zscore=True,threshold=1.96)
matrix.to_csv("/home/vanessa/Documents/Work/BRAINBEHAVIOR/neurovault_z_nothresh.tsv",sep="\t")


