from os import path
from pprint import pprint 
import profile
import re
import unittest

from logbro.statistics.score_calc import ScoreCalcConsumer
from logbro.util.common_subseq import find_all_common_subseq


TOKEN_RE = re.compile('[\w@_\.\:-]+', re.IGNORECASE)
line_sample_to_analyze = open('example_logline.txt').read();

def _split_tokens(s): return TOKEN_RE.findall(s)

def main():

    test_sample = _split_tokens(line_sample_to_analyze);
    stats = ScoreCalcConsumer(line_sample_to_analyze)
    
    with open("example.log", "r") as example_log:
    
        # for tracking the progress
        size_of_example_log = path.getsize("example.log")
        last_flick = -1
        
        for line in example_log:
            
            # track the progress
            progress_ratio = example_log.tell() * 100 / size_of_example_log
            if progress_ratio <> last_flick:
                print "Progress:", progress_ratio, "%"
                last_flick = progress_ratio
            
            if line == line_sample_to_analyze:
                continue

            common_tokens = find_all_common_subseq(test_sample, _split_tokens(line), 1)
            if len(common_tokens) == 0:
                continue
            
            stats.consumeStat(common_tokens)

        stats.summarizeStat()
 
# profile.run('main()')
main()

# -------- UNIT TESTS --------

class TestSplitTokens(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertEqual(_split_tokens('abc cde'), ['abc', 'cde'])

    def test_parse_email(self):
        self.assertEqual(_split_tokens('mail:olksy.lists@gmail.com/password:qwerty'),
                         'mail:olksy.lists@gmail.com password:qwerty'.split(' '))

    def test_lower_upper_case_mix(self):
        self.assertEqual(_split_tokens('mail:Olksy.Lists@Gmail.com/password:qwerty'),
                         'mail:Olksy.Lists@Gmail.com password:qwerty'.split(' '))
 
    def test_numbers_mix(self):
        self.assertEqual(_split_tokens('mail:Olksy0123456.Lists@Gmail.com/password:qwerty'),
                         'mail:Olksy0123456.Lists@Gmail.com password:qwerty'.split(' '))

