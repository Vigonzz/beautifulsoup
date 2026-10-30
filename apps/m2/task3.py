# Violet Gonzalez
# Professor Cristina Videira Lopes
# 262P SWE Programming Styles


#Task 3: Print every tag that exist in the document


import time
import sys, os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer 

# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task3.py <file>\n")
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
strainer = SoupStrainer(True)

# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, parser, parse_only=strainer)

# Find every tag
all_tags = soup.find_all(True)

for tag in all_tags:
    print(tag.name)

print(f"total count of tags: {len(all_tags)}")

# Get the time duration
end = time.perf_counter()
duration = end - start

print(f"That took {duration:.2f} seconds")
