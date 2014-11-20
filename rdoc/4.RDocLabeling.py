#!/usr/bin/env python2

# After download .tar.gz from pubmed, we now want to search the articles for
# the RDoC terms! We want to calculate the probability of a paper belonging to a particular concept group.

import pubmed
import glob
import os
import tarfile
import rdoc
import pickle

start = int(sys.argv[1])        # Start index of files to extract
end = int(sys.argv[2])          # End index of files to extract
papers_directory = sys.argv[3]  # Folder with pubmed targz files
output_file = sys.argv[4]

# We need to look up the PMCIDs associated with the article names, as a UID

# Select a subset from the papers directory
targz = glob.glob(papers_directory + "/*.tar.gz")
targz = targz[start:end]

# Create rdoc parser - currently only supports negative_valence construct
# Will need to tweak and develop new features for different constructs
# Could also do supervised learning of features :)
parser = rdoc.rdoc()

# Extract constructs from papers!
result = parser.extract_construct(targz)

# Save to pickle - we will put them all together after
pickle.dump(result,open( output_file, "wb"))
