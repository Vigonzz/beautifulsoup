# Milestone-2


### Part 1 - Time tracking for SoupStrainer:

| Task | Test File | Version | Count | Script timer | time total |
| :--: | :--: | :--: | :--: | :--: | :--: |
| Task 3 | sample-15mb.xml | MileStone 1 (no Strainer) | 589225 | 4.95s | 6.034s |
| Task 3 | sample-15mb.xml | MileStone 2 (SoupStrainer) | 589225 | 4.92s | 6.088s |
| Task 4 | sample-15mb.xml | MileStone 1 (no strainer) | 98204 | 4.86s | 7.42s |
| Task 4 | sample-15mb.xml | MileStone 2 (SoupStrainer) | 98204 | 4.84s | 7.39s |


- The times are virtually the same due to the file containing an id attribute to every `<record>` including everything nested inside it. So the strainer keeps, almost entirely, the whole document. 

- The strainer is matching every tag so there is nothing getting skipped. The slight time difference is attributed to normal behavior for time runs

### Part 2 - API Definitions:

The following table provides a clear understanding of where each bs4 API used within MileStone 1 and part 1 are located, within the source code. When reading the table, you will see the column line are referenced in comparison the the original unmodified source at our init repo commits. Finding each  API was straightforward thanks to git grep, which is used to quickly search for specific text. Since some names had several matched, I choose the one with the Tag.

| API | File | Line | Class | Used in |
|:--- | :--  | :--: | --: | --: |
| BeautifulSoup (class) | `bs4/__init__.py` | 133 | BeautifulSoup (extends Tag) | All MileStone 1 tasks contain these and all of part 1 of this MileStone task |
| `BeautifulSoup.__init__` | `bs4/__init__.py` | 209 | BeautifulSoup | All MileStone 1 task AND ALL MileStone part 2 application |
| e_only | `bs4/__init__.py` | 214 | BeautifulSoup | MileStone one task 8 and now mileStone 2, milestone part 1 |
| Strainer (class) | `bs4/__init__.py` | 313 | SoupStrainer (extends Element Filter) | MileStone 1 Task 8 and MileStone 2 part 1 |
| `Strainer.__init__` | 345 | SoupStrainer | Milestone 1 task 8 and MileStone 2 part 1 |
| find_all | bs4/element.oy | 2715 | tag | MileStone task 2-8 and MileStone part 1 |
| find | bs4/element.py | 2684 | tag | MileStone 1 task 5 |
| get | bs4/element.py | 2160 | tag | MileStone 1 task 2,4,5 |
| `__setitem__ (tag["class"] = …)` | bs4/element.py | 2223 | tag | (read) | MileStone task 7
| name (tag.name = ...) | bs4/element.py | 1648 | `tag (set in __init__, line 1618)` | MileStone 1 task 6 (assigning), task 3, and task 4 |
| prettify | bs4/element.py | 2601 | tag | MileStone 1 tasks 1,6,7 |
| get_text | bs4/element.py | 524 | PageElement (inherited by tag) | MileStone 1 task 5 |
| find_parent | bs4/element.py | 992 | PageElement (inherited by tag) | MileStone task 5 |
| find_parents | bs4/element.py | 1022 | PageElement (inherited by tag) | Discussed in the MileStone 1 README, but never called | 


### Part 3 - SoupReplacer and What has changed:
When examining the new files (and existing ones) a new API appears named SoupReplacer. The purpose of SoupReplacer is to be similar to SoupStrainer with an important exception, it replaces during parsing as opposed to the after. There are many advantages for conducting replacements and adding such as the not having traverse the whole tree when conducting those changes.

The following files have been changed:
 - filter.py
    - the class
 - `__init__.py` 
    - added to import
    - the constructor
    - parameter
    - handle_starttag
    - handle_endtag

## How to Run Task6.py:
To run task6.py an output folder needs to be made to collect the changed files. After creating our output folder perform the following:

- Open the terminal and turn on the enviornment
    - cd path/to/beautifulsoup
    - source venv/bin/activate (for mac)
    - source venv/Scripts/activate (for windows git bash)
- Now change directories to the output folder
    - command will be python followed by the scripts full path, then the input files full path:
        - python /User/me/path/to/beautifulsoup/apps/m2/task6.py /User/me/path/to/inputFile
- You should see the following when the application is run:
    - Using xml file: (for .xml files) or Using lxml for everything else.
    - A count message for the blockquote tags
    - File name and the duration it took to write
    - a new file (new file name) and its location (output folder)


#### Some Design choices:
- Despite the usefulness of ElmentFilter I did not inherit from it, I wanted to stay as clean to the expectations of the assignment while not altering unnecessary parts. 

- It should be noted that the SoupStrainer comes before the SoupReplacer; therefore, the strainer is deciding what is being kept while the replacer simply renames what is kept. As a user that means:
    - Using SoupStrainer("blockquote") plus the same replacer will not keep any of the `<b>` tags, due to the strainer checking them while they are still named "b"

- While examing the files, you may notice that the endtag needs to be swapped. The endtag needs to be swapped due to the closing tag not being allocated to the right spot. This behavior is caused by  the process of SoupStrainer and SoupReplacer. The start tag has been created yet, the parser would still report the end tag as "b". The lack of change from the parser would trigger _popToTag to not close the tag due to not finding an open "b" tag, thus the blockquote will stay open, and the text "after" will end up inside. **Test 2 catches this behavior and will FAIL when the endtag swap is removed from the application.**

- There is a lack of SoupStrainer `__all__` in the bs4 code, therefore I did not add SoupReplacer in it as to stay consistent with how the SoupStrainer is handled. 

#### Limitations:
Since the parser skips handle_starttag it does not work with html5lib

#### Tests Preformed:
There are two tests that exist within the file, test_soupreplacer.py. 
- The first test covers locating all of the `<b>` tags and replacing them with blockquotes. 
- The Second test covers a check on the end tag, to ensure it closes properly and does not have content after the original end stay
    - Test 2 will fail without the end-tag swap mentioned in design choices. 


#### Failed Test:
There were four sets of failed tests upon opening the application, hence, they existed before any changes were made.

FAILED bs4/tests/test_htmlparser.py::TestHTMLParserTreeBuilder::test_rejected_input
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_real_xhtml_document
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_processing_instruction
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_out_of_range_entity
