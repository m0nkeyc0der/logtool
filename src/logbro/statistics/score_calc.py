"""
Reorganizes the incoming data flow into final statistics
"""

from operator import attrgetter
from pprint import pprint 
import unittest

from logbro.statistics.roles import AbstractConsumer
from logbro.statistics.score import ScoreItem


class ScoreCalcConsumer (AbstractConsumer):
    
    def __init__(self, init_piece):
        
        AbstractConsumer.__init__(self, init_piece)
        self._statistics = {}

    def consumeStat(self, common_tokens):
        
        key = repr(common_tokens)
        
        try:
            self._statistics[key].log_plus_one_more_occurrence()
        except (KeyError):
            self._statistics[key] = ScoreItem(common_tokens, self._init_piece)

    def summarizeStat(self):
        print "*** score calc results ***"
        pprint([x.for_pprint() for x in sorted(self._statistics.values(),
                                               key=attrgetter("similarity_rank"),
                                               reverse=True)])

class TestScoreCalcConsumer(unittest.TestCase):
    
    def test_for_not_being_abstract(self):
        ScoreCalcConsumer("Putin Khuylo")
    
    def test_calc_rank(self):
        
        sc = ScoreItem(common_tokens=[['user']]);
        self.assertAlmostEqual(sc.similarity_rank, 4.0)
        
    def test_calc_rank_2(self):
        
        sc = ScoreItem(common_tokens=[['user', 'boo']])
        self.assertAlmostEqual(sc.similarity_rank, 7.0)

    def test_calc_rank_3(self):
        
        sc = ScoreItem(common_tokens=[['user'], ['boom']])
        self.assertAlmostEqual(sc.similarity_rank, 32 ** 0.5)
