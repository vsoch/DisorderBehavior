#!/usr/bin/env python2

# This script will download pubmed papers for a given start and end index in the current
# ftp manifest file
# Usage : download_pubmed_muhaha.py start end download_folder

import sys
import pubmed
from utils import read_pmid_groups

# Get the start and end index of ids from the command line
start = int(sys.argv[1])
end = int(sys.argv[2])
download_folder = sys.argv[3]
email = sys.argv[4]

# First we need to download full article text
# Create a pubmed object
pm = pubmed.Pubmed(email)

# Get pubmed ids for articles in database
pc_ids = list(pm.ftp["PMCID"])

# Filter down to indices that we want
pc_ids = pc_ids[start:end]

# Download the articles!
pm.download_pubmed(pc_ids,download_folder)
