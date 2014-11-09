#!/usr/bin/env python2

# This script will extract regional voxel counts for a set of thresholded statistical maps

import imageutils as utils
import glob
#from visualize import feature_plots

# Create a new Atlas instance to hold our atlas maps
atlas = utils.Atlas()

# Here our our images to get features for
files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs/*.nii.gz")
output_file = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/regional_features_Z1pt96.tsv"

# Extract features
# specifying the threshold will normalize all images to Z scores, and apply the threshold
threshold = 1.96
df = atlas.count_voxels_in_atlas(mrs=files,output_file=output_file,normalize_threshold=threshold)

# Make plots of results

# Resample standard space image to 8x8x8 mm voxel
standard = "/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/brainbehavior/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz"
standard8mm = utils.resize_image(standard,[8,8,8])

# Now let's extract a matrix of normalized values
# IN PROGRESS! :D

