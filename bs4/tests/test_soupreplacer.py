


import pytest

from . import (
    SoupTest,
)

from bs4 import SoupReplacer

class TestSoupReplacer(SoupTest):
    """ This test covers if the tag replacement from SoupReplacer actually works
    without affecting the nearby tags and if the end of the tag closes properly """

    def test_replace_tag_name(self):
        """ Locates all of the <b> tags and replaces them with blockquote """
        b_to_block = SoupReplacer("b", "blockquote")
        html_string = "<div><b id='greeting'>Hello</b> human! Today we are <b>visiting</b> earth. We <b>hope</b> you prepare for our arrival.</div>"
        soup = self.soup(html_string, replacer=b_to_block)

        assert len(soup.find_all("b")) == 0

        assert len(soup.find_all("blockquote")) == 3
        
        html_check = soup.find("blockquote")

        assert html_check.get("id") == 'greeting'
    
    def test_tag_close_properly(self):
        """ Checking that the end tag closes properly, where content
        after the original end stays outside the new tag """
        end_tag_replacer = SoupReplacer("b", "blockquote")
        end_html ="<p>Hi <b>bold</b> after</p>"
        soup = self.soup(end_html, replacer=end_tag_replacer)

        end_check = soup.find("blockquote")

        assert end_check.get_text() == "bold"

        assert end_check.next_sibling == " after"

    def test_name_xformer_renames_b(self):

        # Test 1:
        check_1 = "<div> <b>Prepare</b> for the career fair!</div>"
        name_xformer_replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
        check_replace = self.soup(check_1, replacer=name_xformer_replacer)

        # No "b" tag left
        assert len(check_replace.find_all("b")) == 0

        # Right num of blockquotes
        assert len(check_replace.find_all("blockquote")) == 1 

        # Test in the right place
        assert str(check_replace.div) == "<div> <blockquote>Prepare</blockquote> for the career fair!</div>"

    def test_attrs_xformer_keeps_href(self):
        # Test 2:
        check_2 = "<div> Look at this super cool website: <a href='https://messenger.abeto.co' class='prim link'>Game Site</a> or even this one <a href='https://codeofsagar.in' class='protfolio'>personal</a> <span id='note'>blah</span></div>"
        # Define what is being kept
        def keep_only_href(tag):
            if tag.name == "a":
                return {"href": tag.get("href")}
            return tag.attrs
        # Replace
        attrs_xformer_replacer = SoupReplacer(attrs_xformer=keep_only_href)
        check_replace_2 = self.soup(check_2, replacer=attrs_xformer_replacer)

        for link in check_replace_2.find_all("a"):
            # Turn an attribute to an attribute dictionary into a list of its keys
            assert list(link.attrs) == ["href"]

        # Span kept its attributes
        assert check_replace_2.span["id"] == "note"
        # Count to make sure both lines are present
        assert len(check_replace_2.find_all("a")) == 2 



