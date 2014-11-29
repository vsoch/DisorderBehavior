#!/usr/bin/env python2

# Now that we have genes associated with papers, we want to try doing meta analysis with NeuroSynth.  First we will just do single genes vs. everything else, THEN we will do groups of disorder associated genes.


import brainbehavior.neurosyn
import brainbehavior.genes as gen
import numpy as np
import re
import glob
import pandas as pd
from lxml import etree
from brainbehavior.pubmed import get_xml_tree, recursive_text_extract, search_text

# Here let's try standard neurosynth analysis

# Now let's group papers by something

# Now let's try just using xyz coordinates
