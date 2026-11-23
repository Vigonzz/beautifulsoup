""" Milestone 4: Iterates over ebery node of an object from BeautifulSoup, one at a time
Although there isn't necessarily a task 8, I just wanted to follow the naming
conventions """

import sys, os
from bs4 import BeautifulSoup, Tag


# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task8.py <file>\n")
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
    parser = 'html.parser'
print(f"Using {parser} File: {filename}")

# Open and parse
# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')

# Counter for nodes
counter = 0
# Test iteration and use isinstance to check rather the node is a tag
for node in soup:
    counter += 1
    if isinstance(node, Tag):
        label = f"<{node.name}>"
    else:
        label = repr(node)
    # Output cleanup:
    print(counter, type(node).__name__, label)


print(f"Visited {counter} nodes")

