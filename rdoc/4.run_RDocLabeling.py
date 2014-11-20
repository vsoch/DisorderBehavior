#!/usr/bin/env python2

# This script will launch instances of 4.RDocLabeling.py
# The output

import os
import pubmed
from utils import read_pmid_groups
import glob

# Here is the folder with the targz files
download_folder = "/scratch/PI/dpwall/DATA/PUBMED/articles"
targz = glob.glob("%s/*.tar.gz",%(download_folder))

# This directory will hold the matrices to parse together
output_dir = "/scratch/PI/dpwall/DATA/pubmed/rdoc/negative_valence

# Submit scripts to parse in batches of 100
start = 0
iters = len(targz)/100

# Prepare and submit a job for each
count = 1
for i in range(0,5000):
  start = i*100
  if i != iters:
    end = start + 100
  else:
    end = len(pc_ids)
  output_file = "%s/%s_rdoc" %(output_dir,count)
  count = count + 1
  jobname = "rdoc_%s-%s" %(start,end)
  filey = open(".job/%s.job" % (jobname),"w")
  filey.writelines("#!/bin/bash\n")
  filey.writelines("#SBATCH --job-name=%s\n" %(jobname))
  filey.writelines("#SBATCH --output=.out/%s.out\n" %(jobname))
  filey.writelines("#SBATCH --error=.out/%s.err\n" %(jobname))
  filey.writelines("#SBATCH --time=2-00:00\n")
  filey.writelines("#SBATCH --mem=12000\n")
  # Usage : download_pubmed_muhaha.py start end download_folder
  filey.writelines("/home/vsochat/python-lapack-blas/bin/python /home/vsochat/SCRIPT/python/brainbehavior/4.RDocLabeling.py %s %s %s %s\n" % (start,end,download_folder,output_file))
  filey.close()
  os.system("sbatch -p dpwall .job/%s.job" % (jobname))
