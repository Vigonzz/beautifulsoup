



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
    


