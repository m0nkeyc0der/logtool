from hashlib import md5;
import json
from operator import attrgetter
import unittest

from logbro.model import TokenSet
from logbro.statistics.score import ScoreItem
from logbro.util.common_subseq import find_all_common_subseq


class LB_IndexError(Exception):  # because IndexError would override build-in one 
    
    def __init__(self, log_bro_says_mgs):
        self._log_bro_says_mgs = log_bro_says_mgs
        
    def __str__(self): return self._log_bro_says_mgs

class Index:
    """
    Index can be stored/loaded into/from JSON string
    
    This is to give the index a chance to be stored in Vim internal variable
    """

    def __init__(self, param):
        """Optionally load index from JSON"""
        
        if isinstance(param, str):
            self._index = json.loads(param)
        else:
            self._index = param
    
    def json_repr(self): return json.dumps(self._index, sort_keys=True)
    def python_repr(self): return repr(self._index)
    
    def slice_for(self, single_line_of_human_readable_repr, orig_buffer, out_buffer):
        
        needle = md5(single_line_of_human_readable_repr).hexdigest()
        
        try:
            for lineN in self._index[needle]:
                
                i = int(lineN)  # Vim always proposes a string for scalars 
                out_buffer.append(orig_buffer[i])
                
        except KeyError:
            # convert it into LB_IndexError
            raise LB_IndexError("No index for this line (key %s)" % needle)
    
class IndexBuilder:
    """
    Acts as statistics builder
    
    Along with Index provides also human readable statistics representation.
    """
    def __init__(self, pattern_string):
        
        self._pattern_string = pattern_string
        self._pattern_ts = TokenSet(pattern_string)
        self._stat = {}
        self._index_under_construction = { "!description": "MD5 hash to log file line numbers mapping" }
        
        # the only purpose of having that is to speed up the code
        self._ts_key_2_md5 = { }  
    
    def feed_line(self, line, line_num):
        """Build up the statistics iteratively"""
        
        common_tokens = find_all_common_subseq(self._pattern_ts, TokenSet(line), threshold=1)
        if len(common_tokens) == 0:
            return
        
        key = repr(common_tokens)
        try:
            
            self._stat[key].log_plus_one_more_occurrence()
            self._index_under_construction[self._ts_key_2_md5[key]].append(line_num)
            
        except (KeyError):

            item = ScoreItem(common_tokens, self._pattern_string)
            self._stat[key] = item
            
            h = md5(item.pretty_pattern()).hexdigest()
            self._ts_key_2_md5[key] = h
            self._index_under_construction[h] = [line_num]
    
    def get_human_readable_repr(self, mask_char=None):
        """
        Gives human-readable statistics representation
        
        Returns a list of strings
        """
        items_sorted = sorted(self._stat.values(),
                              key=attrgetter("similarity_rank"),
                              reverse=True)
        
        return [it.pretty_pattern(mask_char) for it in items_sorted]
    
    def get_index(self):
        """Returns Index object"""
         
        return Index(self._index_under_construction)


class TestIndex(unittest.TestCase):

    def test_init_with_data(self):
        
        ind = Index([1, 2, {"x": "y"}])
        self.assertEqual(ind._index, [1, 2, {"x": "y"}])

    def test_init_with_json(self):
        
        ind = Index('[1, 2, {"x": "y"}]')
        self.assertEqual(ind._index, [1, 2, {"x": "y"}])

    def test_init_with_broken_json(self):
        
        with self.assertRaises(ValueError):
            Index('[1, 2, {"x":_"y"}]')
            
    def test_json_repr(self):
        
        ind = Index([1, 2, {"x": "y"}])
        self.assertEqual(ind.json_repr(), '[1, 2, {"x": "y"}]')

class TestIndexBuilder(unittest.TestCase):

    def test_human_readable_repr(self):

        ib = IndexBuilder("abc  cde *fgi")
        
        ib.feed_line("lalalala", 0)
        ib.feed_line("hello world!", 1)
        ib.feed_line("123123 abc abc cde", 2)
        ib.feed_line("", 3)
        ib.feed_line("no common tokens", 4)
        ib.feed_line("123123 abc abc cde", 5)
        ib.feed_line("fgi", 3)
        
        # achtung! fragile stuff
        self.assertEquals(list(ib.get_human_readable_repr()),
                          # ['abc  cde.....', '  2 occurrence(s)', '..........fgi', '  1 occurrence(s)'])
                          ['abc  cde.....', '..........fgi'])

    def test_HRR_more(self):
 
        ib = IndexBuilder("ACEDebug Summary UserConfig::detectStyle - N.E - entry")
         
        ib.feed_line("ACEDebug Summary UserConfig::detectStyle - N.E - entry", 0)
        ib.feed_line("ACEDebug Summary UserConfig::detectStyle - M.M. - entry", 1)
         
        hrr = ['ACEDebug Summary UserConfig::detectStyle - N.E - entry',
               'ACEDebug Summary UserConfig::detectStyle.........entry']
         
        self.assertEqual(ib.get_human_readable_repr(), hrr)

    def test_index(self):

        ib = IndexBuilder("abc  cde *fgi")
        
        ib.feed_line("lalalala", 0)
        ib.feed_line("hello world!", 1)
        ib.feed_line("123123 abc abc cde", 2)
        ib.feed_line("fgi", 3)
        ib.feed_line("blah blah fgi", 4)
        
        # a fragile regex as soon as json_repr() will give pretty printed
        regex = '^\{.*?, "c1b3f5460a73a0f4c86a818abeb65baf": \[2\], "f453470167a7bf46f5944a3d37caebad": \[3, 4\]\}$'
        
        self.assertRegexpMatches(ib.get_index().json_repr(), regex)

