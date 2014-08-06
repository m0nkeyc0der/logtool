"""
Reorganizes the incoming data flow into final statistics
"""

from pprint import pprint 
import unittest

from logbro.statistics.roles import AbstractConsumer


class SimpleConsumer (AbstractConsumer): 

    def __init__(self, init_piece):
        
        AbstractConsumer.__init__(self, init_piece)
        self._statistics = {}

    def consumeStat(self, common_tokens):
        
        key = repr(common_tokens)
        
        try:
            self._statistics[key] = self._statistics[key] + 1
        except (KeyError):
            self._statistics[key] = 1

    def summarizeStat(self):
        print pprint(self._statistics)
    
    
class TestSimpleConsumer(unittest.TestCase):
    
    def test_for_not_being_abstract(self):
        SimpleConsumer("Putin Khuylo")
