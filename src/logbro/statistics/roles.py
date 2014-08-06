"""Defines logtool.statistics.Consumer role"""

import abc
import unittest


class AbstractConsumer(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, init_piece):
        self._init_piece = init_piece

    @abc.abstractmethod
    def consumeStat(self, common_tokens): pass

    @abc.abstractmethod
    def summarizeStat(self): pass
    

class TestAbstractConsumer(unittest.TestCase):
    
    def test_for_being_abstract(self):
        with self.assertRaises(TypeError):
            AbstractConsumer("Putin Khuylo")