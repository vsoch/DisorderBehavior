# BrainBehavior 

This module will work with four databases that combined can make inferences about disorders and behaviors:

- NeuroVault: functional and structural group analyses
- Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
- NeuroSynth: mining literature for behavioral concepts to produce brain maps
- Pubmed: Where the papers live!


### Disorders Represented in NeuroSynth
*What areas of the brain have been published to have aberrancy for a robust set of neuropsychiatric disorders?*

The script 1.NeuroSynthDisorderTag.py reads in a list of disorders defined by the cognitive atlas, and searches for the terms in the abstracts of the entire corpus of NeuroSynth articles.  Returned is a matrix with "1" indicating the term is present, and "0" if not.  Common words (disorder, syndrome, etc.) are removed.  The script 2.parseDisorderMatrix.R then reads in this result file, and outputs lists of pmids associated with each disorder, for use in the next step.

## Meta Analysis with Disorder Papers
We next use 3.NeuroSynthMeta.py to run meta analysis with the lists of disorder papers.  We produce a set of brain images for each disorder: forward inference (pAgF, probability of activation given the feature), and reverse inference (pFgA, probability of the feature given activation).

TODO: A script / method to compare these maps!

*UNDER DEVELOPMENT*


### Disorders Represented in NeuroVault
*Can we summarize a database of group neuroimages? What patterns do we see? Can we map on disorders, concepts?*

The script downloadMetaNeuroVault.py will download meta information as well as complete images represented in NeuroVault.  Then, the scripts R/mrToMNI.R and R/MNIToMNI.R will create a huge matrix of images by voxels.

TODO: Need to intelligently threshold the values, normalize, and prepare for unsupervised clustering (this means labels, values, etc.)
