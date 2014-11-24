#!/usr/bin/env python2

# This script will read in rdoc pickle files from a directory, parse,
# and return as one matrix.

import glob
from rdoc import parse_pickle_results

# Here are the rdoc files
rdoc_files = glob.glob("/scratch/PI/dpwall/DATA/PUBMED/rdoc/negative_valence/*rdoc.pkl")

# Parse result into matrix
parse_pickle_results(rdoc_files)
