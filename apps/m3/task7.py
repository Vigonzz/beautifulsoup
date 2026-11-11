# This program sets class="test" onto every <p> tag. This occurs during parsing
# using SoupReplacer
# The M3 version of M1 task7, python task7.py <input file>

import sys, os, time
from bs4 import BeautifulSoup, SoupReplacer

def set_p_class(tag):
    if tag.name == "p":
        tag.attrs["class"] = "test"

# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task7.py <file>\n")
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

# Build the replacer 
p_replacer = SoupReplacer(xformer=set_p_class)

# Start the timer
start = time.perf_counter()

# Open and parse
# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, parser, replacer=p_replacer)
    
# Stop the timer 
end = time.perf_counter()

# Turns a parse tree into a into a formatted string
pretty = soup.prettify()

# Building the path for the output
base_name = os.path.basename(filename)
name, ext = os.path.splitext(base_name)

# saves the file 
new_name = f"{name}_task7_m3{ext}"

output_path_m3 = new_name

# Write the output
with open(output_path_m3, "w", encoding="utf-8") as write_file:
    write_file.write(pretty)

# Get the time duration 
duration = end - start

print(f"Wrote {output_path_m3} in {duration:.2f} seconds")



