from pyscr.frontend import Validator
from pyscr.structure import Mapper
import unittest


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.sut = Validator()

    def makeTable(self, name='tableName', columns=[], index=False):
        return Mapper(name=name, columns=columns, index=index)

    def makeColumn(self, name='colA', datatype='int', is_optional=False, is_const=False):
        return Mapper(name=name, datatype=datatype, is_optional=is_optional, is_const=is_const)

    def testCanValidateColumnNumber(self):
        example = Mapper(columns=[self.makeColumn()])
        self.assertTrue(self.sut(example))
        example = Mapper(columns=[])
        self.assertRaises(Validator.NoColumnsProvided, self.sut, example)

    def testCanValidateColumnNameUniqness(self):
        colA = self.makeColumn(name='colA')
        example = Mapper(columns=[colA])
        self.assertTrue(self.sut(example))
        example = Mapper(columns=[colA, colA])
        self.assertRaises(Validator.NonUniqueColumnNames, self.sut, example)
