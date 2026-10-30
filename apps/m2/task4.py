# Violet Gonzalez
# Professor Cristina Videira Lopes
# 262P SWE Programming Styles


# Task 4: 
#   With a single API call, print out all the tags that have an id attribute
# this version will be using the mILEsTONE 2 SoupStrainer version


import time
import sys, os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task4.py <file>\n")
    sys.exit(1)

# create a name for the file
filename = sys.argv[1]

# if statement to check if the file exist:
if not os.path.isfile(filename):
    sys.stderr.write(f"{filename} does not exist\n")
    sys.exit(1)

# determine the file type
if filename.lower().endswith(".xml"):
    parser = "xml"
else:
    parser = "lxml"
print(f"Using {parser} File: {filename}")

start = time.perf_counter()

# Creating the strainer
strainer = SoupStrainer(id=True)

# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, parser, parse_only=strainer)

# Find every tag
id_attr = soup.find_all(id=True)

for tag in id_attr:
    print(tag.name)
    print(tag.get('id'))

print(f"total count of tags: {len(id_attr)}")

# Get the time duration
end = time.perf_counter()
duration = end - start

print(f"That took {duration:.2f} seconds")