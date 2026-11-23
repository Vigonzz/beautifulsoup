""" Test cases for MileStone 4 """

import pytest
from collections.abc import Iterator
from types import GeneratorType
from . import SoupTest
from bs4 import BeautifulSoup
from bs4.element import (
    Tag,
    NavigableString,
    Comment,
    Doctype,
)


class TestSoupIteration(SoupTest):
    """ Test the soup iteration implemented in the init, that 
    loops through the doc, saves the successor, yields, then moves the
    successor"""

    def test_iteration_on_nested_tags(self):
        """ Using depth-first for doc order, iterate over the soup and visits every tag"""
        
        nested_html = "<div><ul><li></li><li></li></ul></div><span></span>"

        # Build the soup
        soup = BeautifulSoup(nested_html, 'html.parser')
        names = []
        # Loop over the soup and append the names to a list
        for node in soup:
            names.append(node.name)

        # The expected results to help with comparisons
        expected = ['div', 'ul', 'li', 'li', 'span']

        # Test the comparison 
        assert names == expected

    def test_on_mixed_nodes(self):
        """ Test iteration on mixed node types. So iterating over the soup 
        should begin to visit the tags, text, comments, and doctype """

        # Create the html string
        testing = "<!DOCTYPE html><div><p>hi</p><!-- note --></div><h1>bye</h1>"
        
        # Build the soup
        soup = BeautifulSoup(testing, 'html.parser')
        
        types = []
        for node in soup:
            types.append(type(node))
        
        expected = [Doctype, Tag, Tag, NavigableString, Comment, Tag, NavigableString]
        
        # Assert that types is the same as our equals
        assert types == expected
    
    def test_empty_doc(self):
        """ Test iteration on empty docs. Therefore the soup should be empty
        and yield nothing thus raising no errors """

        # Instead of creating an HTML string as per last time we are going to
        # just use an empty one
        soup = BeautifulSoup("", 'html.parser')
        # Create a counter
        count = 0

        for node in soup:
            count += 1
        
        # Assert that the count is going to equal 0
        assert count == 0
    

    def test_is_lazy_and_restartable(self):
        """ Iteration is to return a lazy iterator, meaning that its not
        a list and that it yields one node at a time. Each loop is also going to
        be starting fresh """

        # Build the soup
        test = "<div><p>hi</p><!-- note --></div><h1>bye</h1>"
        soup = BeautifulSoup(test, 'html.parser')
        # Use an iterator not a list
        iterator = iter(soup)

        # Is not a list
        assert not isinstance(iterator, list)
        # Get the iterator the soup provides. This is what a for loop calls
        assert isinstance(iterator, Iterator)
        # Since a list iterator is also an Iterator, only generator, proves the nodes are produced lazily by yield
        assert isinstance(iterator, GeneratorType)

        # Get one node at a time
        first = next(iterator)

        assert first.name == "div"

        # Store another node now
        second = next(iterator)

        assert second.name == "p"

        # See changes made mid loop
        # Create a new tag
        footer = soup.new_tag("footer")
        soup.append(footer)

        # Keep using the same iterator
        remaining = []
        for node in iterator:
            remaining.append(node.name)

        # The list was built in advance, it wont contain the footer since it was 
        # added after he iteration had begun. This proves that nodes are found on demand

        # Looping twice will ensure we are starting new without continuing 
        first_count = 0
        second_count = 0

        for _ in soup:
            first_count += 1
        
        for _ in soup:
            second_count += 1

        # Assert our loop provided the expected amount of lines
        assert first_count == 7
        assert second_count == 7

    def test_tag_unchanged(self):
        """ Instead of yielding the descendants iterating over a regular tag 
        should just yield the direct children """

        test = "<div><p>hi</p><!-- note --></div><h1>bye</h1>"
        soup = BeautifulSoup(test, 'html.parser')

        # Get the div
        div = soup.contents[0]

        # Collect all of the children nodes
        children = []
        for node in div:
            children.append(node)
        
        # Assert how many children node exist
        assert len(children) == 2
        # Assert which tags are included
        assert children == div.contents
        # Assert the specific tags that should not be included
        assert "hi" not in children