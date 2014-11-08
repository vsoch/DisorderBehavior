#!/usr/bin/python

# This script will parse the RDOC matrix.  We want to produce a data structure that holds, for each construct,
# a list of "evidence" terms that can be searched for in pubmed articles to create a feature vector for the
# article that represents some "evidence" for the article belonging to the construct.

from bs4 import BeautifulSoup
from urllib2 import urlopen
import unicodedata

# Grab the html RDoC tables
url = "http://www.nimh.nih.gov/research-priorities/rdoc/rdoc-constructs.shtml"
html = urlopen(url).read()
soup = BeautifulSoup(html, "lxml")
tables = soup.findAll("table")

# Here is a function to convert from unicode to str
def uniTostr(string):
  return unicodedata.normalize('NFKD', string).encode('ascii','ignore').strip(" ")

# Parse using beautiful soup
data = []
for t in tables:
  # First parse the header
  thead = t.findAll('th')
  title = thead.pop(0)
  domain_idx = title.text.find("Domain:")
  construct_idx = title.text.find("Construct:")
  subconstruct_idx = title.text.find("Subconstruct:")
  domain = title.text[domain_idx:construct_idx].replace("Domain:","").replace("\n","")
  if subconstruct_idx:
    subconstruct = title.text[subconstruct_idx:len(title.text)].replace("Construct:","").replace("\n","")
    construct = title.text[construct_idx:subconstruct_idx].replace("Construct:","").replace("\n","")
  else: 
    construct = title.text[construct_idx:subconstruct_idx].replace("Construct:","").replace("\n","")
    subcontruct = unicode("")
  
  # Convert from unicode to string
  domain = uniTostr(domain)
  construct = uniTostr(construct)
  subconstruct = uniTostr(subconstruct)

  # Now get the rest of the header
  header = []
  for h in range(2,len(thead)):
    header.append(uniTostr(thead[h].text))

  header = header + ["Domain","Construct","Subconstruct"]
  # Now parse the table contents
  tbody = t.findAll('tbody')
  contents = []
  for b in tbody:
    rows = b.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [uniTostr(c.text) for c in cols]
      [contents.append(c) for c in cols]
      if contents:
        contents = contents + [domain,construct,subconstruct]
      data.append(contents)


# Add the header (should be same for all tables)
print "Adding Header:" + str(header)

# STOPPED HERE - need to figure out subconstruct, and why there is extra text at bottom

# Write to tab separated file
filey = open("data/RDoCMatrix.tab","w")
filey.writelines("\t".join(header) + "\n")
for d in data:
  filey.writelines("\t".join(d) + "\n")

filey.close()
