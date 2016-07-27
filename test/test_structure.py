from pyscr import Mapper, DataType, Column, Index, Table
import unittest


class TestMapper(unittest.TestCase):

    def testCanSetNamedAttributesInCtor(self):
        sut = Mapper(a='X', b=0, c=[1], d=True)
        self.assertEqual(sut.a, 'X')
        self.assertEqual(sut.b, 0)
        self.assertEqual(sut.c, [1])
        self.assertEqual(sut.d, True)

    def testCanSetNamedAttributesAfterCtor(self):
        sut = Mapper()
        sut['a'] = 'X'
        sut['b'] = 0
        self.assertEqual(sut.a, 'X')
        self.assertEqual(sut.b, 0)

    def testCanReadItems(self):
        sut = Mapper(a='X', b=0)
        self.assertTrue('a' in sut)
        self.assertTrue('b' in sut)
        self.assertFalse('x' in sut)
        self.assertEqual(sut['a'], 'X')
        self.assertEqual(sut['b'], 0)


class TestDataType(unittest.TestCase):

    def testCanCreateDataTypes(self):
        self.assertEqual('string', DataType.string)
        self.assertEqual('int', DataType.int)
        self.assertEqual('bool', DataType.bool)
        self.assertEqual('float', DataType.float)

    def testThrowsWhenWrongArgPassed(self):
        self.assertRaises(ValueError, DataType, 'invalid')


class TestColumn(unittest.TestCase):

    def testCanCreateColumn(self):
        col = Column(
            name='colName', datatype='int', is_optional=True, is_const=True)
        self.assertEqual(col.name, 'colName')
        self.assertEqual(col.datatype, DataType.int)
        self.assertTrue(col.is_optional)
        self.assertTrue(col.is_const)
        col = Column(name='colName', datatype=DataType.bool)
        self.assertEqual(col.datatype, DataType.bool)


class TestIndex(unittest.TestCase):

    def testCanCreateIndex(self):
        idx = Index(name='idxName', columns=('colA', 'colB'))
        self.assertEqual(idx.name, 'idxName')
        self.assertEqual(len(idx.columns), 2)
        self.assertTrue('colA' in idx.columns)
        self.assertTrue('colB' in idx.columns)


class TestTable(unittest.TestCase):

    def testCanCreateTable(self):
        colA = Column(name='colA', datatype=DataType.int)
        colB = Column(name='colB', datatype=DataType.string)
        table = Table(name='tableName', columns=(colA, colB))
        self.assertEqual(table.name, 'tableName')
        self.assertEqual(table.columns.colA.name, 'colA')
        self.assertEqual(table.columns.colA.datatype, DataType.int)
