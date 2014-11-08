#!/usr/bin/env python2

# This script will extract regional voxel counts for a set of thresholded statistical maps

import imageutils as utils
import glob

# Create a new Atlas instance to hold our atlas maps
atlas = utils.Atlas()

# Here our our images to get features for
files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs/*.nii.gz")
output_file = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/regional_features.tsv"

# Extract features
df = atlas.count_voxels_in_atlas(mrs=files,output_file=output_file)
