#!/usr/bin/env python2

# This script will use the BrainBehavior.py module to download meta information about images and collections from NeuroVault

from brainbehavior import neurovault
nv = NeuroVault()

# Print all image and collections metadata to outfile
image_outfile = "data/NeuroVaultImageMeta.tab"
collections_outfile = "data/NeuroVaultCollectionsMeta.tab"
nv.exportMeta(image_outfile)
nv.exportCollections(collections_outfile)

# Download images to file
outfolder = "/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs"

# Now use R/summarizeData.R to explore distributions, etc.
nv.downloadImages(outfolder)
