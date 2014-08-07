'''
Knuth-Morris-Pratt string matching
David Eppstein, UC Irvine, 1 Mar 2002
 
from http://code.activestate.com/recipes/117214/
from http://en.wikibooks.org/wiki/Algorithm_Implementation/String_searching/Knuth-Morris-Pratt_pattern_matcher#Python
'''

import unittest


def _KnuthMorrisPratt_find_iter(pattern, text):
 
    '''
    Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string.find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield.
    '''
 
    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)
 
    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift
 
    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            yield startPos

def contains(needle, haystack):
    
    first_pos = next(_KnuthMorrisPratt_find_iter(needle, haystack), None)
    
    return not first_pos is None

class TestKmtForString(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertTrue(contains('abc', 'abc cde fgi'))

    def test_contains_middle_seq(self):
        self.assertTrue(contains('cde', 'abc cde fgi'))

    def test_contains_end_seq(self):
        self.assertTrue(contains('fgi', 'abc cde fgi'))

    def test_contains_oversized_seq(self):
        self.assertFalse(contains('abc cde fgi!', 'abc cde fgi'))

    def test_contains_iteslf(self):
        self.assertTrue(contains('abc cde fgi', 'abc cde fgi'))

class TestKmtForList(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertTrue(contains('ab c'.split(' '), 'ab c cde fgi'.split(' ')))

    def test_contains_middle_seq(self):
        self.assertTrue(contains('cd e'.split(' '), 'abc cd e fgi'.split(' ')))
 
    def test_contains_end_seq(self):
        self.assertTrue(contains('f gi'.split(' '), 'abc cde f gi'.split(' ')))
 
    def test_contains_oversized_seq(self):
        self.assertFalse(contains('abc cde fgi fgi'.split(' '), 'abc cde fgi'.split(' ')))
 
    def test_contains_iteslf(self):
        self.assertTrue(contains(*['abc cde fgi'] * 2))