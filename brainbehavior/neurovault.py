#!/usr/bin/env python

"""

NeuroVault: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

from utils import DataJson
import string
import urllib2
import json
import numpy as np
from utils import DataJson

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Matthew Sacchet (msacchet@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"


class NeuroVault:
    def __init__(self):
      self.images = self.__getMeta__()                  # get image meta information
      self.collections = self.__getCollections__()      # get collections meta information from json
      print self

    """Download meta information about images in database"""
    def __str__(self):
      return "NeuroVault Object (nv) Includes <nv.images,DataJson><nv.collections,DataJson>}"

    """Export meta directly to tab separated file"""
    def exportMeta(self,outfile):
      if not self.images:
        self.images = self.__getMeta__()
      self.images.__export__(outfile)
      
    """Export collections directly to tab separated file"""
    def exportCollections(self,outfile):
      if not self.collections:
        self.collections = self.__getCollections__()
      self.collections.__export__(outfile)

    """Download image data to file"""
    def downloadImages(self,outdir):
      import urllib; import ntpath
      if not outdir:
        print "Downloading images to current working directory."
      else:
        print "Downloading images to " + outdir
        if outdir[-1] not in ["\\","/"]:
          outdir = outdir + "/"
        filegetter = urllib.URLopener()
        for image in self.images.data["file"].values():
          filename = ntpath.basename(image)
          # Get the collection id
          collection_id = self.images.data["collection"][image].split("/")[-2].encode("utf-8")
          output_image = outdir + collection_id + "_" + filename
          if not os.path.isfile(output_image):
            print "Downloading " + filename + "."
            try:
              filegetter.retrieve(image, output_image)
            except:
              print "Error downloading " + image + ". Skipping!"

# Internal functions * * * *

    """Download image meta"""
    def __getMeta__(self):
      print "Extracting NeuroVault images meta data..."
      # Return a DataJson object with all fields
      myjson = DataJson("http://neurovault.org/api/images/","file")
      print "Images:"
      print myjson
      return myjson

    """Download collection meta"""
    def __getCollections__(self):
      print "Extracting NeuroVault collections meta data..."
      # Return a DataJson object with all fields
      myjson = DataJson("http://neurovault.org/api/collections/","id")
      print "Collections, see\n NeuroVault.collections.fields\nNeuroVault.collections.data"
      print myjson
      return myjson

def main():
  print __doc__

if __name__ == "__main__":
  main()
