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


class Validator(object):

    class Error(Exception):

        def __init__(self, msg): self.message = msg

        def __str__(self): return str(self.message)

    class NonUniqueColumnNames(Error):

        def __init__(self, msg):
            super(Validator.NonUniqueColumnNames, self).__init__(
                'multiple definitions of %s!' % str(msg))

    class NoColumnsProvided(Error):

        def __init__(self):
            super(Validator.NoColumnsProvided, self).__init__(
                'no column definitions provided!')

    def __init__(self): pass

    def __call__(self, table):
        self.checkColumnNumber(table)
        self.checkColumnNames(table)
        return True

    def checkColumnNumber(self, table):
        if len(table.columns) == 0:
            raise Validator.NoColumnsProvided

    def checkColumnNames(self, table):
        names = tuple(map(lambda x: x.name, table.columns))
        duplicates = [d for d in names if names.count(d) > 1]
        if duplicates:
            raise Validator.NonUniqueColumnNames(','.join(set(duplicates)))
