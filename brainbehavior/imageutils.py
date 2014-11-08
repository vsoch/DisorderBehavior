#!/usr/bin/env python

"""

imageutils: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import nibabel
import glob
import numpy as np
import pandas as pd
from scipy import ndimage
from nilearn.image import resample_img
import os

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Matthew Sacchet (msacchet@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"


# Atlas Summary Object -------------------------------------------------------------------
"""Atlas - internal object for storing atlas labels and regions, for use to summarize the 
regional patterns of different spatial maps"""
class Atlas:
  def __init__(self,atlas_lookup="data/atlas/atlasFeatures.tab",atlas_directory="data/atlas",standard="data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz"):
    self.read_standard(standard)
    self.read_atlas_images(atlas_directory,atlas_lookup)

  """Read atlas images into nifti objects - only keep those in MNI 152 space"""
  def read_standard(self,standard):
    print "Loading standard space..."
    self.standard = nibabel.load(standard)
    affine = self.standard.get_affine()
    shape = self.standard.shape[:3]
    self.mask = self.standard.get_data() > 1e-13

  """Read atlas images into nifti objects - only keep those in MNI 152 space
  Atlas lookup should be a tab separated file, with each line having the image name,
  label, and pixel value in the map.  Atlas images should be in the atlas directory."""
  def read_atlas_images(self,atlas_directory,atlas_lookup):
    print "Reading in list of atlas images."
    self.atlas_data = dict()
    self.atlas_labels = pd.read_csv(atlas_lookup,sep="\t")
    unique_images = list(np.unique(self.atlas_labels["image"]))
    for image in unique_images:
      print "Reading atlas image %s" % (image)
      full_path = os.path.abspath("%s/%s" % (atlas_directory,image))
      header = nibabel.load(full_path)
      header = resample_img(header, target_affine=self.standard.get_affine(),target_shape=self.standard.shape[:3])
      img = header.get_data()
      self.atlas_data[image] = img

  """Get voxel count feature vector for one or more images against all of atlas labels"""
  def count_voxels_in_atlas(self,mrs,output_file):
    feature_vectors = []
    for mr in mrs:
      print "MR image is %s" %(mr)
      feature_labels = []
      feature_vector = []
      full_path = os.path.abspath("%s" % (mr))
      header = nibabel.load(full_path)
      # Only do for single timepoint images for now
      if len(header.shape) == 3:
        header = resample_img(header, target_affine=self.standard.get_affine(),target_shape=self.standard.shape[:3])
        img = header.get_data()
        # For each label in the atlas, get a voxel count
        for atlas_image,image_data in self.atlas_data.iteritems():
          atlas_labels_subset = self.atlas_labels.ix[self.atlas_labels.index[self.atlas_labels["image"]==atlas_image]]
          print "Atlas image is %s" %(atlas_image)
          for row in atlas_labels_subset.iterrows():
            voxel_value = row[1]["label"]
            region_label = row[1]["regionName"]
            feature_labels.append("%s_%s" % ( atlas_image, region_label ))
            region_mask = image_data == voxel_value
            region_mask = np.logical_and(region_mask, self.mask)
            voxel_count = np.sum(np.logical_and(region_mask, img).astype(np.int))
            feature_vector.append(int(voxel_count))
        feature_vectors.append(feature_vector)
      df = pd.DataFrame(feature_vectors,columns=feature_labels)
      df.to_csv(output_file,sep="\t")
    return df
