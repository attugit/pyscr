from pyscr import Syntax, FrontEnd, NonUniqueColumnNames, InvalidColumnsInIndex
import unittest


class SyntaxTest(unittest.TestCase):

    def setUp(self):
        self.sut = Syntax()
        self.fe = FrontEnd()

    def testCanCreateSyntaxFromValidParsedContext(self):
        example = """
        table tableName
        column colA int
        column colB string optional
        column colC bool const
        column colD float const optional
        """
        table = self.sut(self.fe(example))
        self.assertEqual(table.name, 'tableName')
        self.assertEqual(len(table.columns), 4)
        self.assertEqual(table.columns.colA.datatype, 'int')
        self.assertFalse(table.columns.colA.is_optional)
        self.assertFalse(table.columns.colA.is_const)
        self.assertEqual(table.columns.colB.datatype, 'string')
        self.assertTrue(table.columns.colB.is_optional)
        self.assertFalse(table.columns.colB.is_const)
        self.assertEqual(table.columns.colC.datatype, 'bool')
        self.assertFalse(table.columns.colC.is_optional)
        self.assertTrue(table.columns.colC.is_const)
        self.assertEqual(table.columns.colD.datatype, 'float')
        self.assertTrue(table.columns.colD.is_optional)
        self.assertTrue(table.columns.colD.is_const)

    def testThrowsWhenColumnsAreNotUniqe(self):
        example = """
        table invalidColumn
        column colA int
        column colB string
        column colA bool
        """
        self.assertRaises(NonUniqueColumnNames, self.sut, self.fe(example))

    def testCanCreateSyntaxFromValidParsedContextWithIndex(self):
        example = """
        table tableName
        index idx (colD, colB)
        column colA int
        column colB string
        column colC bool
        column colD float
        """
        table = self.sut(self.fe(example))
        self.assertTrue(table.index)
        self.assertEqual(table.index.name, 'idx')
        self.assertEqual(len(table.index.columns), 2)
        self.assertEqual(table.index.columns[0], 'colD')
        self.assertEqual(table.index.columns[1], 'colB')

    def testThrowsWhenIndexHaveInvalidColumns(self):
        example = """
        table invalidTable
        index idx (colE, colA)
        column colA int
        column colB string
        """
        self.assertRaises(InvalidColumnsInIndex, self.sut, self.fe(example))