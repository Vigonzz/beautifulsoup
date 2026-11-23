# Milestone-4

## Quick overview of functionality and purpose
Milestone 4 allows for BeautifulSoup to become iterable over every node within the tree. The premise of use should follow:
- Create the soup
- Loop over the soup to acquire each node, one at a time


## Milestone 4: Technical Brief
Violet Gonzalez
Professor Cristina Videira Lopes
Course 262P Programming Styles
November 22, 2026


##### **What is iterable BeautifulSoup:**
Before the implementation of iterable to BeautifulSoup, this feature allows For every note to be iterable within the tree. When putting this implementation of iteration and use the loop will actually acquire all notes as opposed to just the top children. When using a test string that is made of pure HTML I noticed that before the milestone four implementation there were only two notes that were printed as the output however, after the milestone for implementationUtilizing the same loop, six nodes were printed and in a very clean format. 

#### **Implementation:**
Within the file `bs4/__init__.py`, a few additions were made to help create the new feature of iteration. The first being the addition of __iter__ to BeautifulSoup (ideally not in Tag.__iter__ as it would disrupt the current intended functionality), the next_element including a generator using yield which allows for the start at the first child and stop at None. From examining the code, it becomes clear that there is no stop node; however, that is intended. Since the soup is at root, there is no purpose to have it included, this would be a direct contrast to .descendants. Lastly, the iteration feature follows a depth-first approach for the document order; an example of this would be if you were to test an html file the first node to appear would be: Doctype ‘html’. 

#### **Why No List is Built:**
There also become the question of why there is no list built. The way this feature was implemented is through linear time meaning that it goes through one node at a time when called.This can also be proved through the test_m4_iteration.py file, specifically test 4, which has the generator and sees the tag appended after the iteration starts. For more clarification the test is constructed as:
- iter(soup) as the generator (calls exactly what a loop will)
- appends the footer tag after the two next() calls, which confirms that the iterator still located it

#### **Design Decisions:**
The design decisions for the implementation of the iteration feature focused on the task at the core and allowed for some error handling. 
- Traversal follows the next_element with the generator previously mentioned. Since bs4 already chains every node in the document order, there is no recursion needed; therefore, documents that have deep trees can be iterated through at no trouble. Using yield also follows the task qualification of not having a list built. 

- Since iterations start at the soup's first child, it seems unnecessary to include the soup which is a hidden wrapper and not even implemented in .descendants, so you won't see it being yielded. 
- Error handling for no document means that the user will just have the iterator yield nothing. This avoids an index error and acts as a double catch for the end of the document as well.

- Save the next node before yielding seemed essential since it can keep the traversal place in case anything was tampered with, like `current` changing or even being removed entirely; therefore, `current.next_element` is stored in `successor` before the yield.

- Each loop is also started fresh meaning each for loop starts from the beginning, if a singular object was used for a second loop the the second loop would just be empty. The generator method will automatically do this without having to reloop. Additionally, this works by taking advantage of the soup acting as a container. 

#### **Testing:**
There are five tests to proves different cases for the implementation of iteration. The first test goes over the depth-first order which is essential for iterating over every tag within the documents order. The second test its range of functionality, therefore, is a document has many different tags each one is handled. The third test goes over the iteration of an empty doc, similar to what was discussed prior; it checks for validation on if the soup is empty, and thus, should  not yield anything or raise errors. A fourth test can be considered the most important one as it shows the behavior of iteration features not being a list. Since it yields one node at a time each loop starts fresh and takes it quite literally one at a time. Lastly the fifth test covers the tags being untouched by iterating over the direct children not the descendants. 

#### **How to Run**
- From the repo root activate the environment. 
- Once the environment is activated, use:
    `python apps/m4/task8.py <path/to/file>` 

NOTE: If using an xml file, ensure that `lxml` is installed for the “xml” parser: pip install `lxml`

The expected output should be:
The parser you are using
The node type
Labels like tags being shown as just the names like `<html>` and strings which are displayed as `repr()` so the text appears in quotes. 
Lastly a count with how many nodes are visited (created through a variable, still no list)

#### **Limitations:**
If you were to use len() and in, it would still refer to the direct children only, from the soup. The iteration feature only applies to itself and did not affect the original usage others. Also if the user were to change the tree ahead of the current node the iteration wouldn't work as that is a contradiction to the successor that was saved. So removing a node would cause the chain of iteration to jump and just result in none sooner than anticipated. 

Formatting from an html file comes with alot of whitespace, which is translated to NavigableString nodes, so it displays as ‘\n’. Inevitably, the `\n` will then be counted as a node since they are real nodes but may not be the ones the user is expecting.
If the user would want to gather the top-level children, then it is important to note that with this implementation modifies that. From iteration the script will instead retrieve all nodes, since again, the behavior is changed and not implemented as new.

#### Thing to expect:
When running pytest use `python -m pytest` and the user should see 4 failed test which existed originally and have no effect to any of the implementations. and primarily 738 test passed.


Acknowledgment:
AI was used to help with debugging, deeper undertsanding, and step by step guide. The full conversation can be viewd at:
https://claude.ai/share/1cc41d75-47dd-4a73-8267-3a5fef3f898a

All code was created by me