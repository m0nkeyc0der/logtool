"""
This is a module to find all common subsequences for a string and a list

The only function it exports is find_all_common_subseq(s1, s2, threshold=3)

The function has been implemented from the scratch and is not optimized at all!
The performance is supposed to suffer as it's complexity is going to be O(m^3*n)

Here is the code review:
http://codereview.stackexchange.com/questions/56464/longest-common-substring-solution-for-a-string-and-a-list
"""
import doctest
import re
import unittest


def _contains(subseq, inseq):
    return any(inseq[pos:pos + len(subseq)] == subseq for pos in range(0, len(inseq) - len(subseq) + 1))

def find_all_common_subseq(s1, s2, threshold=3):

    all_of = []
    
    def is_inner_seq(i, j):
        return any(k < i < j <= l or k <= i < j < l for k, l in all_of)

    for i in range(0, len(s1)):
        for j in range(i + threshold, len(s1) + 1):

            if _contains(subseq=s1[i:j], inseq=s2):
                all_of.append((i, j))  # add a tuple to work OK when s1, s2 are lists

    only_outer_seq = filter(lambda tup: not is_inner_seq(tup[0], tup[1]),
                            all_of)

    return [s1[i:j] for i, j in only_outer_seq]

def pretty_highlight(instr, all_css, mask_char=None):
    """
    Mask with dots '.' everything but all_css tokens
    
    Args:
    instr   -- string for pattern to highlight matches from all_css
    all_css -- iterable for match
    """
    
    if mask_char is None:
        mask_char = '.'
    
    template = [mask_char] * len(instr)  # need this as a mutable string
    
    for css_token in all_css:
        
        try:
            # allow css_token be responsible of it's regex representation 
            match = re.search(css_token.__regex__(), instr)
        except (AttributeError):
            match = re.search(re.escape(css_token.__str__()), instr)
        
        if match is None:
            raise LookupError("Error looking up CSS token '%s' in enclosing string '%s'"
                              % (css_token, instr))
            
        template[match.start():match.end()] = list(match.group())
    
    # return as string
    return ''.join(template)

class TestContainsForString(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertTrue(_contains('abc', 'abc cde fgi'))

    def test_contains_middle_seq(self):
        self.assertTrue(_contains('cde', 'abc cde fgi'))

    def test_contains_end_seq(self):
        self.assertTrue(_contains('fgi', 'abc cde fgi'))

    def test_contains_oversized_seq(self):
        self.assertFalse(_contains('abc cde fgi!', 'abc cde fgi'))

    def test_contains_iteslf(self):
        self.assertTrue(_contains('abc cde fgi', 'abc cde fgi'))

class TestContainsForList(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertTrue(_contains('ab c'.split(' '), 'ab c cde fgi'.split(' ')))

    def test_contains_middle_seq(self):
        self.assertTrue(_contains('cd e'.split(' '), 'abc cd e fgi'.split(' ')))
 
    def test_contains_end_seq(self):
        self.assertTrue(_contains('f gi'.split(' '), 'abc cde f gi'.split(' ')))
 
    def test_contains_oversized_seq(self):
        self.assertFalse(_contains('abc cde fgi fgi'.split(' '), 'abc cde fgi'.split(' ')))
 
    def test_contains_iteslf(self):
        self.assertTrue(_contains(*['abc cde fgi'] * 2))

class Test_FindAllCommonSubseq(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertEqual(find_all_common_subseq('abc cde fgi', 'fgiabcab'), ['abc', 'fgi'])
        
    def test_for_inner_substr(self):
        self.assertEqual(find_all_common_subseq('abc cde fgi', 'fgiabcab', threshold=2),
                         ['abc', 'fgi'])
        
    def test_simple_list(self):
        self.assertEqual(find_all_common_subseq([11, 22, 33, 44, 55, 66, 77, 88],
                                                [22, 33, 44, 44, 55, 66, 77]),
                         [[22, 33, 44], [44, 55, 66, 77]])

class TestPrettyHighlight(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(pretty_highlight('abc cde fgi', ['abc', 'fgi']),
                         'abc.....fgi')
        
    def test_simple(self):
        self.assertEqual(pretty_highlight('abc cde fgi', ['cde']),
                         '....cde....')
        
    def test_metachar(self):
        with self.assertRaises(LookupError):
            pretty_highlight('abc cRe fgi', ['c.e'])
        
    def test_negative(self):
        with self.assertRaises(LookupError):
            pretty_highlight('abc cde fgi', ['XX', 'YY'])
        
    def test_regex_capable_path(self):
        
        class BoomError (Exception): pass
        class RegexCapable:
            def __regex__(self):
                raise BoomError("Try to catch me!")
        
        with self.assertRaises(BoomError):
            pretty_highlight('abc cde fgi', ['abc', RegexCapable()])
        
    def test_regex_capable(self):
        
        class RegexCapable:
            def __regex__(self): return re.compile('[fgi]{3}')
        
        self.assertEqual(pretty_highlight('abc cde fgi', ['abc', RegexCapable()]),
                         'abc.....fgi')
        
    def test_regex_capable_2(self):
        
        class RegexCapable:
            def __regex__(self): return '[fgi]{3}'
        
        self.assertEqual(pretty_highlight('abc cde fgi', ['abc', RegexCapable()]),
                         'abc.....fgi')
        
if __name__ == '__main__':

    doctest.testmod()
    unittest.main(verbosity=2)
