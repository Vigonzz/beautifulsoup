# Violet Gonzalez
# Professor Cristina Videira Lopes
# 262P SWE Programming Styles


# Task 6: Change all the <b> tags to <blockquote> tags and write the tree onto a file.

import time
import sys, os
from bs4 import BeautifulSoup
from bs4 import SoupReplacer

# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task6.py <file>\n")
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

# Create the replacer
b_to_blockquote = SoupReplacer("b", "blockquote")

# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, parser, replacer=b_to_blockquote)

print(f"Changed blockquote tags in the output file")

# Turns a parse tree into a into a formatted string
pretty = soup.prettify()

# Building the path for the output
base_name = os.path.basename(filename)
name, ext = os.path.splitext(base_name)

# saves the file 
new_name = f"{name}_task6{ext}"

output_path = new_name

# Write the file 
with open(output_path, "w", encoding="utf-8") as write_file:
    write_file.write(pretty)

# Get the time duration
end = time.perf_counter()
duration = end - start

print(f"Wrote {output_path} in {duration:.2f} seconds")

