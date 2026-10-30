# Violet Gonzalez
# Professor Cristina Videira Lopes
# 262P SWE Programming Styles


# Task 2 Print out all the hyperlinks (<a> tags).
import time
import sys, os
from bs4 import BeautifulSoup

# check the arguments being passed
if len(sys.argv) < 2:
    sys.stderr.write("Need input of: python3 task2.py <file>\n")
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

# Read the file passing it into Beautiful Constructor 
with open(filename, encoding="utf-8") as f:
    soup = BeautifulSoup(f, parser)

#find the anchor tags
find_links = soup.find_all("a")

for link in find_links:
    url = link.get("href")
    if url is None:
        print("No href")
    else:
        print(url)

print(f"total count of links: {len(find_links)}")

# Get the time duration
end = time.perf_counter()
duration = end - start

print(f"That took {duration:.2f} seconds")
