


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

    def test_xformer_removes_class(self):
        """ Test 3: the class delete """
        check_3 = "<div class='delete'> Delete the following paragraph> <p class='paragraph'> The robots are in town.<span class='spanning' id='ah'> Robots </span></p></div>"
        
        # The helper function
        def remove_class_attr(tag):
            if "class" in tag.attrs:
                # Delete the key from the function 
                del tag.attrs["class"]

        # Arrange the replacer
        xformer_replacer = SoupReplacer(xformer=remove_class_attr)
        check_replace_3 = self.soup(check_3, replacer=xformer_replacer)

        assert len(check_replace_3.find_all(class_=True)) == 0

    # Proves the order Test 4
    def test_all_three_xformers_run_in_order(self):
        """ Test 4 test the xformers"""
        check_4 = "<p> I would <b>enjoy</b> a quick snack.</p>"

        # The helpers
        rename_b = lambda tag: "blockquote" if tag.name == "b" else tag.name

        def mark_renamed(tag):
            if tag.name == "blockquote":
                attrs_xformer_copy = (dict(tag.attrs))
                attrs_xformer_copy["data-renamed"] = "yes"
                return attrs_xformer_copy
            return tag.attrs
    
        # xformer
        def mark_seen(tag):
            if "data-renamed" in tag.attrs:
                tag.attrs["data-seen"] = "yes"

        # The replacer 
        all_three_replacer = SoupReplacer(name_xformer=rename_b, attrs_xformer=mark_renamed, xformer=mark_seen)
        check_replace_4 = self.soup(check_4, replacer=all_three_replacer)

        len(check_replace_4.find_all("b")) == 0
        bq = check_replace_4.blockquote
        bq["data-renamed"] == "yes"
        bq["data-seen"] == "yes"

    # Test 5 Validation errors:
    def test_invalid_args_raise(self):
        """ Test bad calls and ensure that the step 2 check catches it """
        with pytest.raises(ValueError):
            SoupReplacer(og_tag="b")

        with pytest.raises(ValueError):
            SoupReplacer("b", "blockquote", xformer=print)

        with pytest.raises(TypeError):
            SoupReplacer(attrs_xformer="hello")
    
    # Test 6 Every tag visited once, root skipped:
    def test_xformer_visits_every_tag(self):
        """ Proves popTag hook reaches every tag """
        check_6 = "<div> I am a nested tag <p><br> When I think of not being nested, I nest more!<span>span</span></p> </div>"

        # Arranging the list and the helper
        visited = []
        
        # helper
        def record(tag):
            visited.append(tag.name)

            check_6_replacer = SoupReplacer(xformer=record)
            check_replace_6 = self.soup(check_6, replacer=check_6_replacer)

            assert len(visited) == len(check_replace_6.find_all(True))
            assert "[document]" not in visited
            assert "br" in visited
            
 
    