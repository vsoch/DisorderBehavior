#!/usr/bin/env python2

# This script will run meta analyses for lists of pmids from groups in the disorder
# matrix created in 1.NeuroSynthDisorderTag.py, and parsed in 2.parseDisorderMatrix.R

import neurosyn as nsy
import numpy as np
import pickle
import glob
from utils import read_pmid_groups

# Create a NeuroSynth Object to perform the meta analysis
ns = nsy.NeuroSynth(8000)
# Or load from file with the decode object created for 3000 terms!
pickle.dump(open("data/8000terms/ns.pkl","rb"))
# ns = pickle.load( open( "/scratch/users/vsochat/DATA/BRAINBEHAVIOR/ns.pkl", "rb" ) )

# Read in the groups (these are)
groups = read_pmid_groups("../output/disorder_pid_groups_thresh15.v3.txt")
metagroups = read_pmid_groups("../output/disorder_pid_groups_thresh15_meta.v3.txt")

## OPTION 1: OUTPUT IMAGES FOR META ANALYSIS -----------------------
outdir = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/DisorderMaps"

# Here we can create output images, or store data in array
# This section will output disorder images
outdir = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/DisorderMaps"
for g,members in groups.iteritems():
  print "Performing meta analysis for disorder " + g
  ns.neurosynthMeta(members,fdr=0.05,outdir=outdir,outprefix=g,image_list="pAgF_z_FDR_0.05")

# Now let's produce the meta analysis images'
outdir = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/MetaDisorderMaps"
for g,members in metagroups.iteritems():
  outprefix = g.replace(",","_")
  print "Performing meta analysis for disorder " + g
  ns.neurosynthMeta(members,fdr=0.05,outdir=outdir,outprefix=outprefix,image_list="pAgF_z_FDR_0.05")

# This section will not
# We will hold data in this array
for g,members in groups.iteritems():
  print "Performing meta analysis for disorder " + g
  images = ns.neurosynthMeta(members)


# OPTION 2: Do decoding of images ----------------------------------
# Here is if we want to decode Now let's decode!
files = glob.glob('/scratch/users/vsochat/DATA/BRAINBEHAVIOR/DisorderMaps/*pAgF_z_FDR*')
files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/DisorderMaps/*FDR_0.01.nii.gz")
ns.decode(files,"data/disorder_decode.v4.txt")
pickle.dump(ns, open( "/scratch/users/vsochat/DATA/BRAINBEHAVIOR/ns8000.pkl", "rb" ) )

files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/MetaDisorderMaps/*FDR_0.05.nii.gz")
ns.decode(files,"data/disorder_decode_meta.v5.txt")

# Here is decoding with topic maps (threshold at 0.5)
# TO DO: write this function to decode with custom set of images!
images = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/DisorderMaps/*FDR_0.05.nii.gz")
mrs = glob.glob("/home/vanessa/Documents/Work/NEUROSYNTH/topicmaps/maps/*FDR_0.05.nii.gz")
ns.decode(files,"data/disorder_decode_topicmaps.txt",mrs)


## OPTION 3: Output pairwise comparisons between images (contrast analysis)
outdir = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/Contrast"
for g1,members1 in groups.iteritems():
  for g2,members2 in groups.iteritems():
    if g1!=g2:
      output_name = g1 + "_gr_" + g2
      print "Contrasting groups %s vs. %s" % (g1,g2)
      ns.neurosynthContrast(members1,members2,fdr=0.05,outdir=outdir,outprefix=output_name,image_list="pAgF_z_FDR_0.05")
