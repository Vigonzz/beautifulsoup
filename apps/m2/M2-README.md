# Milestone-2

Baseline:
pytest -rf -q | grep FAILED:
FAILED bs4/tests/test_htmlparser.py::TestHTMLParserTreeBuilder::test_rejected_input
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_real_xhtml_document
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_processing_instruction
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_out_of_range_entity

### Part 1 - Time tracking for SoupStrainer:

| Task | Test File | Version | Count | Script timer | time total |
| :--: | :--: | :--: | :--: | :--: | :--: |
| Task 3 | sample-15mb.xml | MileStone 1 (no Strainer) | 589225 | 4.95s | 6.034s |
| Task 3 | sample-15mb.xml | MileStone 2 (SoupStrainer) | 589225 | 4.92s | 6.088s |
| Task 4 | sample-15mb.xml | MileStone 1 (no strainer) | 98204 | 4.86s | 7.42s |
| Task 4 | sample-15mb.xml | MileStone 2 (SoupStrainer) | 98204 | 4.84s | 7.39s |


- The times are virtually the same due to the file containing an id attribute to every `<record>` including everything nested inside it. So the strainer keeps, almost entirely, the whole document. 

- The strainer is matching every tag so there is nothing getting skipped. The slight time difference is attributed to normal behavior for time runs

### Part 2- API Definitions:

The following table provides a clear understanding of where each bs4 API used within MileStone 1 and part 1 are located, within the source code. When reading the table, you will see the column line are referenced in comparison the the original unmodified source at our init repo commits. Finding each  API was straightforward thanks to git grep, which is used to quickly search for specific text. Since some names had several matched, I choose the one with the Tag.

| API | File | Line | Class | Used in |
|:--- | :--  | :--: | --: | --: |
| BeautifulSoup (class) | bs4/__init__.py | 133 | BeautifulSoup (extends Tag) | All MileStone 1 tasks contain these and all of part 1 of this MileStone task |
| BeautifulSoup.__init__ | bs4/__init__.py | 209 | BeautifulSoup | All MileStone 1 task AND ALL MileStone part 2 application |
| e_only | bs4/__init__.py | 214 | BeautifulSoup | MileStone one task 8 and now mileStone 2, milestone part 1 |
| Strainer (class) | bs4/__init__.py | 313 | SoupStrainer (extends Element Filter) | MileStone 1 Task 8 and MileStone 2 part 1 |
| Strainer.__init__ | 345 | SoupStrainer | Milestone 1 task 8 and MileStone 2 part 1 |
| find_all | bs4/element.oy | 2715 | tag | MileStone task 2-8 and MileStone part 1 |
| find | bs4/element.py | 2684 | tag | MileStone 1 task 5 |
| get | bs4/element.py | 2160 | tag | MileStone 1 task 2,4,5 |
| __setitem__ (tag["class"] = …) | bs4/element.py | 2223 | tag | (read) | MileStone task 7
| name (tag.name = ...) | bs4/element.py | 1648 | tag (set in __init__, line 1618) | MileStone 1 task 6 (assigning), task 3, and task 4 |
| prettify | bs4/element.py | 2601 | tag | MileStone 1 tasks 1,6,7 |
| get_text | bs4/element.py | 524 | PageElement (inherited by tag) | MileStone 1 task 5 |
| find_parent | bs4/element.py | 992 | PageElement (inherited by tag) | MileStone task 5 |
| find_parents | bs4/element.py | 1022 | PageElement (inherited by tag) | Discussed in the MileStone 1 README, but never called | 



