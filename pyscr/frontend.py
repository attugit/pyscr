from pyparsing import CaselessKeyword
from pyparsing import Word
from pyparsing import Optional
from pyparsing import Literal
from pyparsing import OneOrMore
from pyparsing import Group
from pyparsing import alphas


class FrontEnd(object):
    delim = Literal(',').suppress()
    lp = Literal('(').suppress()
    rp = Literal(')').suppress()
    table = CaselessKeyword(
        'table').suppress() + Word(alphas).setResultsName('table')
    index = CaselessKeyword('index').suppress() + \
        Group(Word(alphas).setResultsName('name') + lp +
              OneOrMore(Word(alphas) + Optional(delim)).setResultsName('columns') +
              rp).setResultsName('index')
    datatype = (CaselessKeyword('int') |
                CaselessKeyword('string') |
                CaselessKeyword('bool') |
                CaselessKeyword('float')).setResultsName('datatype')
    opmode = Optional(
        CaselessKeyword('optional').setResultsName('is_optional'))
    cvmode = Optional(CaselessKeyword('const').setResultsName('is_const'))
    mode = opmode & cvmode
    column = CaselessKeyword('column').suppress() + \
        Group(Word(alphas).setResultsName('name') +
              datatype + mode).setResultsName('column')

    def __init__(self):
        self.grammar = FrontEnd.table + \
            Optional(FrontEnd.index) + \
            OneOrMore(FrontEnd.column).setResultsName('columns')

    def __call__(self, text):
        return self.grammar.parseString(text)