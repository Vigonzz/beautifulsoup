# Milestone-3


## Milestone 3: SoupReplacer transformer
add functions that help transform the tags during parsing. 


| File | What Changed |
| :---: | :---: |
| `bs4/filter.py` | `SoupReplacer` has the constructor extended, three with three xformer arguments + validation. A new transformer method is also included |
| `bs4/__init__.py` | hook in popTag line 792 |
| `bs4/tests/tests_soupreplacer.py` | Implemented six new tests |
| `apps/m3/task7.py` | new application |
| Technical Brief | End of the README.md |

### Understanding the API:
The constructor signature:
SoupReplacer(og_tag=None, alt_tag=None, name_xformer=None, attrs_xformer=None, xforer=None)

Each xformer receives and returns the following:
Tag in:
| xformer | receives/returns |
| :---: | :---: |
| `name_xformer` | New name |
| `attrs_xformer`| New attrs dict |
| `xformer` | Nothing |

Order:
name -> attrs -> xformer

| Validation Rules|
| :---: |
| half pair -> ValueError |
| pair + xformer -> ValueError |
| non-callable -> TypeError |

The return guards in transform have to be non-empty string, attrs must be a dict. 

### Design decision:
The reason for using popTag is due to transformers needing the tag object, while also not being able to run before its created. Also if we were to rename while the tag is open then it would break the open_tag_counter and end tag matching. Running in PopTag helps bookkeeping and skips the root document, the only side effect that is showed is that the children are transformed before the parents are. 

### Tests:
| Test # | Test | What is checks | What is proves |
| :---: | :---: | :---: | :---:|
| 1 | `test_name_xformer_renames_b` | `name_xformer` lambda renames `<b>` to `<blockquote>`; thus remaining as no b left, one blockquote, and the text after the tag stays outside it | `name_xformer` works, and the close-time hook will avoid M2’s end-tag bug without having to touch `handle_endtag` |
| 2 | `test_attrs_xformer_keeps_only_href` | an `attrs_xformer` will strip every attribute except for href from the `<a>` tags. Also the `<span id="note">` is then left untouched | `attrs_xformer` replaces attributes, and conditions on the tag’s name only affect the intended tags |
| 3 | `test_xformer_removes_class` | an `xformer` will delete classes from nested tags while the id survives | `xformer` works through side effects, reaches nested tags, and only removes what is targeted |
| 4 | `test_all_three_xformers_run_in_order` | chains order, where each steps leaves a marker so the next depends on it | runs in the document order so each will see the previous changes |
| 5 | test_invalid_args_raise | `pytest.raises` on a half pair, pair + xformer, and a non-callable|The validation from the constructor will reject bad args with the appropriate error types |
| 6 | `test_xformer_visits_every_tag` | The `xformer` will record every tag name it sees and compares it against all tags in the soup | every tag is visited exactly once while the root doc is skipped, and children are transformed before parents |


Teh metrics: 
727 passed, 4 failed, 107 Skipped. The 727 is from M2 and the 6 new test.
The following test failed:
===== short test summary info ======
FAILED bs4/tests/test_htmlparser.py::TestHTMLParserTreeBuilder::test_rejected_input - Failed: DID NOT RAISE ParserRejectedMarkup
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_real_xhtml_document - AssertionError
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_processing_instruction - AssertionError
FAILED bs4/tests/test_lxml.py::TestLXMLTreeBuilder::test_out_of_range_entity - AssertionError

### The App:
This application which is task7. sets class = "test" on every `<p>` tag during parsing by using `xformer`. 

##### To Run:
use:
python apps/m3/task7.py `<input file>`

The results you will be expecting to see are identical to the output of M1 tasks just at a slightly, very small speed increase (M1 = 0.09, M3 = 0.05). You can also validate this by using diff to compare each. 


## Technical Brief
Violet Gonzalez
Professor Cristina Videira Lopes
Course 262P Programming Styles
November 9, 2026

Milestone 3: Technical Brief

What is SoupReplacer:
SoupReplacer holds a significant impact on how parsing is handled. Specifically, SoupReplacer allows for tags to be changed while parsing, instead of the base behavior of parsing first and walking the tree afterward.  The main importance of changing tags while parsing means that the document goes through one pass instead of two (with base behavior). When looking at the differences from Milestone 1 task 7 (loops after parsing) compared to M3 task 7 (replaces during parsing) it gave exactly the same output yet with a small time difference. Milestone 1 task 7 provided a time of 0.09 when running a test file whereas Milestone 3 task 7 provided a time of 0.05 for the same file.

M2 API (SoupReplacer(og_tag, alt_tag)):
The functionality of Milestone 2’s API: SoupReplacer(og_tag, alt_tag), is to swap the tag names before the tag is created in handle_starttag; there is then a translation for the end tag in handle_endtag. More specifically, the parser will read the raw text and essentially report the events to BeautifulSoup but only one event at a time. With each report the tree begins to build with handle_starttag as the start of the event and thus handle_endtag as the end. However, there is a quirk, handle_endtag, needs to translate “b” to “blockquote” before running _popToTag, to find and close the right tag. The reasoning behind this quirk is due to handle_endtag asking bs4 to close the most recent open tag name “b” but since it was changed there is no open tag named b anymore, therefore, nothing gets closed and “after” will end up inside the actual blockquote. In terms of comparison, it’s relatively easy to use because when the tag is created with its new name, the rules of bs4 (per tag rules contain whitespace handling and even void tags) apply to the new name. This replacer is also hard to misuse due to its simplicity leaving little room for misunderstanding of its use case and implementation. Yet referring back to the quirk mentioned, this replacer can be buggy quickly without the proper handling for the end-tag thus needing changes in two methods. There is also the point of limitations in where there can only be one name swap, following with no room for attributes or conditions. 

M3 API SoupReplacer(name_xformer, attrs_xformer, xformer):
With the milestone 3 API parsing follows the normal bs4 events: bs4 creates the tag as a normal b and when the tag is open, pushTag counts the tag under “b” and follows the typical behavior of bs4. The endtag, handle_endtag(“b”), does not need a translation such as the previous milestone which needed a translation phase. Instead, the transformer is applied in popTag once the tag is closed, therefore, the parser logic never sees a renamed tag. When a user uses milestone 3, they are able to pass up to the three functions defined, where it renames, edits the attribute, and more; the replacer combines these functions into a single transformation. However, each function receives the tag as the previous one left it since it runs in its fixed order. Test 4 enacts this behavior by building a chain where each step depends on the previous. There are pros to the API of milestone 3, such as the freedom, or expressiveness provided through the ability for functions to receive the whole tag, so changes can depend on attributes or content, which is not available through milestone 2. Additionally, there is simplicity in milestones 3 use, since every tag passes through the popTag so then one hook covers every tag. Also differing from Milestone 2, the children, here, finish first, since when the parents’ xformer runs it means the whole subtree has already been completed. However, there are still cons that exist, such as the builder rules. Since pushTag decides the void and whitespace handling (discussed in milestone 2) when the tag opens, renaming at close time doesn’t update those rules, so the tag keeps the original name’s handling. Also parsing speed depends on the function’s speed, meaning if there was a slow function then the whole parse will run slow. Due to the increase in flexibility with xformer, there is more of a risk, since it can change anything it reaches, so it should be used with caution.  

Shared Limitations:
It is important to understand that there are limitations to what is supported. Html5lib builds the tree through its adapter so it is attaching tags directly without calling handle_starttag or popTag. Therefore neither SoupReplacer nor parse_only works with it, and since parse_only was already unsupported there, it matched existing bs4 behavior. Another limitation involves, SoupStrainer tells bs4 only to keep certain tags so if the user was to have: parse_only=SoupStrainer(“a”) then the a tags are going to be kept while everything else will be thrown away, which is normal behavior but should be noted so there is no expectation of the strainer seeing a renamed tag. The replacer runs in popTag, but tags the strainer filters out are never created, so they never reach popTag and are never transformed. Also, since the strainer runs at start time, before any renaming has occurred, it will check the original tag names. Therefore, if a strainer was looking for a replaced name, it would keep nothing due to the tag being called the original name. 

Recommendation:
I recommend that we ship both interfaces. While each interface has its pros and cons, it would be limiting on behalf of the user to choose one over the other. The pair interface from milestone 2 creates a straightforward use case, and since the tag is created with its new name, the rules from bs4 apply appropriately. Ideally, the user would not need much functionality, and therefore, stick to a simple rename, which protects them from the pitfalls offered from xformers, such as a slow function slowing down the entire parse. However, there will be cases in which the user can benefit from the milestone 3 xformers, which allows for checks in attributes and content, while also avoiding end-tag bugs due to its close-tine hook. So having the first interface for users allows for non-intensive tasks such as a simple renaming, while not leaving out more technical users from exploring and utilizing our more involved interface. Note, keeping both satisfies user needs but creates more documentation and maintenance due to the two code paths. The cost of more documentation and slightly more maintenance is not enough to neglect the potential of serving a larger user base. 


Acknowledgment:
AI was used to help with debugging, deeper undertsanding, and step by step guide. The full conversation can be viewd at:
https://claude.ai/share/d4cbdbcb-44d4-493d-b234-12a15fb85f03

ALL code was done by me. 