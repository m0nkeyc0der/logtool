import re
import unittest

from logbro.model import TokenSet
from logbro.util.common_subseq import pretty_highlight


class ScoreItem:

    def __init__(self, common_tokens, the_pattern_string=None):
        self.token_set = common_tokens
        self.num_occurrences = 1
        self.similarity_rank = self._calc_rank(common_tokens)
        self.the_pattern = the_pattern_string
        
    def log_plus_one_more_occurrence(self):
        self.num_occurrences = self.num_occurrences + 1

    def for_pprint(self): 
        
        class RegexCapableTokenSet(list):
            def __init__(self, linstance): super(RegexCapableTokenSet, self).__init__(linstance)
            def __regex__(self):
                return re.compile('.*?'.join(re.escape(t) for t in self))
        
        result = vars(self)
        
        pp = self.pretty_pattern()
        if not pp is None:
            result['the_pattern'] = pp
        
        return result
    
    def pretty_pattern(self, mask_char=None):

        if self.the_pattern is None:
            return

        re_capable = [TokenSet(ts) for ts in self.token_set]
        return pretty_highlight(self.the_pattern, re_capable, mask_char)

    def _calc_rank(self, common_tokens):
        """ Standard "distance" function to calculate rank """
        return sum(sum(len(token) for token in token_seq) ** 2 for token_seq in common_tokens) ** 0.5;
    
class TestScoreItem(unittest.TestCase):
    
    def test_calc_rank(self):
        
        sc = ScoreItem(common_tokens=[['user']]);
        self.assertAlmostEqual(sc.similarity_rank, 4.0)
        
    def test_calc_rank_2(self):
        
        sc = ScoreItem(common_tokens=[['user', 'boo']])
        self.assertAlmostEqual(sc.similarity_rank, 7.0)

    def test_calc_rank_3(self):
        
        sc = ScoreItem(common_tokens=[['user'], ['boom']])
        self.assertAlmostEqual(sc.similarity_rank, 32 ** 0.5)
