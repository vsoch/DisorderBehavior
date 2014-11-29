#!/usr/bin/env python2

# This script will read in rdoc pickle files from a directory, parse,
# and return as one matrix.

import glob
from rdoc import parse_pickle_results

# Here are the rdoc files
rdoc_files = glob.glob("/scratch/PI/dpwall/DATA/PUBMED/rdoc/negative_valence/*rdoc.pkl")

# Parse result into matrix
parse_pickle_results(rdoc_files)

# Some manual work to deal with non utf8 characters
def myfunction(row):

newframe = list()
for row in test.iterrows():
   try:
     newrow = list(row[1])
     newrow = [str(x).encode('utf-8') for x in newrow]
     newframe.append(newrow)
   except:
     print "Can't add row"

towfique raj

filey = open("/scratch/PI/DATA/PUBMED/rdoc/negative_valence_result_matches!.csv","w")
filey.writelines("\t".join(test.columns))
filey.writelines("\n")
for row in newframe:
  filey.writelines("\t".join(row) + "\n")



