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

import os
import nibabel
import glob
import numpy as np
import pandas as pd
from scipy import ndimage
from nilearn.image import resample_img
from nilearn.masking import apply_mask

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Matthew Sacchet (msacchet@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"



"""Resamples image voxels to different voxel size, should be a tuple with three values
returns a nibabel.nifti1.Nifti1Image"""
def resize_image(input_image,voxel_dimension):
  if len(voxel_dimension) != 3:
    print "Please specify a list of three voxel sizes, e.g. (3,3,3)"
    return

  # If we have a filename, we need to load it
  if isinstance(input_image,str):
    header = nibabel.load(input_image)
  # Or we can take a nibabel nifti1 image
  elif isinstance(input_image,nibabel.nifti1.Nifti1Image):
    header = input_image
  else:
    print "Please provide an input_image filepath OR nibabel.nifti1.Nifti1Image object!"
    return
  voxel_dimension = tuple(voxel_dimension)
  target_affine = np.diag(voxel_dimension)
  resampled = resample_img(header, target_affine=target_affine)


"""A wrapper for spatial_normalize_image - returns a pandas dataframe of image voxels normalized (resampled) to another (assuming standard) space"""
def spatial_normalize_images(input_images,standard):
  image_matrix = []
  for mr in input_images:
    transformed_image = spatial_normalize_image(mr,standard)
    image_matrix.append(transformed_image["data"])
  df = pd.DataFrame(image_matrix,columns=input_images)
  return df

"""Transform a single image into another space (likely a standard we are assuming both in MNI space!)"""
def spatial_normalize_image(image,standard):
   standard = read_image(standard)
   image = read_image(image)
   header = resample_img(image["header"], target_affine=standard["affine"],target_shape=standard["shape"])
   transformed = header.get_data()
   return {"data":transformed,"mask":transformed > 1e-13,"shape":header.shape[:3],"affine":header.get_affine(),"file":image,"header":header}

"""Returns an image in the Zscore space, thresholded at threshold"""
def normalize_image_zscore(header,threshold=None):
  data = header.get_data()
  Z = (data - np.mean(data)) / np.std(data)
  if threshold:
    mask = Z < float(threshold)
    Z[mask] = float(0)
    # Return the new header object
  return nibabel.Nifti1Image(Z,header.get_affine())

"""Reads in image, returns image values and mask"""
def read_image(image_file):
    print "Loading image %s" %(image_file)
    mr = nibabel.load(image_file)
    affine = mr.get_affine()
    shape = mr.shape[:3]
    data = mr.get_data()
    mask = data > 1e-13
    mr = {"data":data,"mask":mask,"shape":shape,"affine":affine,"file":image_file,"header":mr}
    return mr

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
    self.standard = read_image(standard)

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
      img = spatial_normalize_image(full_path,self.standard["file"])
      self.atlas_data[image] = img

  """Get voxel count feature vector for one or more images against all of atlas labels
If normalize_threshold is specified, will convert image to Z score, and threshold at value"""
  def count_voxels_in_atlas(self,mrs,output_file,normalize_threshold=False):
    feature_vectors = []
    for mr in mrs:
      print "MR image is %s" %(mr)
      feature_labels = []
      feature_vector = []
      full_path = os.path.abspath("%s" % (mr))
      header = nibabel.load(full_path)
      # Only do for single timepoint images for now
      if len(header.shape) == 3:
        header = resample_img(header, target_affine=self.standard["affine"],target_shape=self.standard["shape"])
        # If the user hasn't specified a normalize_threshold, just take image data as is'
        if normalize_threshold:
          header = normalize_image_zscore(header,normalize_threshold)
        img = header.get_data()
        # For each label in the atlas, get a voxel count
        for atlas_image,image_data in self.atlas_data.iteritems():
          atlas_labels_subset = self.atlas_labels.ix[self.atlas_labels.index[self.atlas_labels["image"]==atlas_image]]
          print "Atlas image is %s" %(atlas_image)
          for row in atlas_labels_subset.iterrows():
            voxel_value = row[1]["label"]
            region_label = row[1]["regionName"]
            feature_labels.append("%s_%s" % ( atlas_image, region_label ))
            # Create the region mask equal to the voxel value for the label
            region_mask = image_data["data"] == voxel_value
            # Add the standard mask
            region_mask = np.logical_and(region_mask, self.standard["mask"])
            voxel_count = np.sum(np.logical_and(region_mask, img).astype(np.int))
            feature_vector.append(int(voxel_count))
        feature_vectors.append(feature_vector)
    df = pd.DataFrame(feature_vectors,columns=feature_labels)
    df.to_csv(output_file,sep="\t")
    return df
