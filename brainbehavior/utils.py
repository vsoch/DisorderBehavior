#!/usr/bin/env python

"""

utils: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"


"""Read in a formatted file with group names and PMID assignments: each line has
a group name followed by a single list of PMIDs - one group per line.  Returns
a lookup dictionary of group"""
def read_pmid_groups(input_file,separator="\t"):
  filey = open(input_file,"r")
  groups = dict()
  for f in filey.readlines():
    group = f.strip("\n").split("\t")
    name = group.pop(0)
    group = [g.strip(" ") for g in group]
    groups[name] = group
  filey.close()
  return groups

# Data Json Object Functions--------------------------------------------------------------
"""DataJson: internal class for storing json, accessed by NeuroVault Object"""
class DataJson:
  def __init__(self,url,keyname):
    self.url = url
    self.keyname = keyname
    self.json = self.__get_json__()
    self.data = self.__parse_json__() 
    self.fields = self.json[0].keys()

  """Print json data fields"""
  def __str__(self):
    return "DataJson Object dj Includes <dj.data:dict,js.json:list,dj.fields:list,dj.url:str,dj.keyname:str>"

  """Get raw json object"""
  def __get_json__(self):
    try:
      tmp = urllib2.urlopen(self.url).read()
      return json.loads(tmp)
    except:
      print "Error download json from url " + self.url + "!"

  """Parse a json object into a dictionary (key = fields) of dictionaries (key = file urls)"""
  def __parse_json__(self):
    if not self.json:
      self.json = self.__get_json__()
    fields = self.json[0].keys()
    # This dictionary will hold dictionaries of variables
    data = dict()
    print "Adding " + str(len(fields)) + " fields "
    for f in fields:
      tmp = dict()
      for j in self.json:
        keyindex = j[self.keyname]
        tmp[keyindex] = j[f]
      data[f] = tmp
    return data

  """Export a DataJson to tab separated file"""
  def __export__(self,outfile):
    if outfile:
      print "Writing data from " + self.url + " to " + outfile
      filey = open(outfile,"w")
      filey.writelines("\t".join(self.fields) + "\n")
      for x in self.json:
        row = []
        for j in self.fields:
          # Unicode
          if isinstance(x[j],unicode):
            row.append(x[j].encode('utf-8')) # This will leave non ascii characters
            # This will filter, but then we are missing letters!
            #content = filter(lambda x: x in string.printable, x[j])
            #row.append(content)
          # Bool, int, or None
          else:
            row.append(str(x[j]))
        filey.writelines("\t".join(row)  + "\n")
      filey.close()
    else:
      print "Please specify an output file!"
