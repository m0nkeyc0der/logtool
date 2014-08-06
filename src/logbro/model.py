import re
import unittest


class TokenSet (list):
    
    _TOKENIZER_RE = re.compile('[\w@_\.\:-]{2,}')

    def __init__(self, param):
        if isinstance(param, list):
            super(TokenSet, self).__init__(param)
        else:
            super(TokenSet, self).__init__(TokenSet._TOKENIZER_RE.findall(param))
        
    def __regex__(self):
        return re.compile('.*?'.join(re.escape(t) for t in self))


class TestTokenSet(unittest.TestCase):
    
    def test_smoketest(self):
        self.assertEqual(TokenSet('abc cde'), ['abc', 'cde'])

    def test_parse_email(self):
        self.assertEqual(TokenSet('mail:olksy.lists@gmail.com/password:qwerty'),
                         'mail:olksy.lists@gmail.com password:qwerty'.split(' '))

    def test_lower_upper_case_mix(self):
        self.assertEqual(TokenSet('mail:Olksy.Lists@Gmail.com/password:qwerty'),
                         'mail:Olksy.Lists@Gmail.com password:qwerty'.split(' '))
 
    def test_numbers_mix(self):
        self.assertEqual(TokenSet('mail:Olksy0123456.Lists@Gmail.com/password:qwerty'),
                         'mail:Olksy0123456.Lists@Gmail.com password:qwerty'.split(' '))
 
    def test_more(self):
        self.assertEqual(TokenSet('ACEDebug Debug UserConfig::detectStyle - N.E - entry'),
                         ['ACEDebug', 'Debug', 'UserConfig::detectStyle', 'N.E', 'entry'])

