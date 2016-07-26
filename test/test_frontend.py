from pyscr.frontend import FrontEnd
import unittest

class TestParser(unittest.TestCase):


    def setUp(self):
        self.sut = FrontEnd()


    def tearDown(self):
        pass


    def testCanParseTableWithoutIndex(self):
        example = """
        table tableName
        column colName int
        """
        ctx = self.sut(example)
        self.assertEqual(ctx.table, 'tableName')
        self.assertFalse(ctx.index)


    def testCanParseTableWithIndex(self):
        example = """
        table tableName
        index indexName (colName)
        column colName int
        """
        ctx = self.sut(example)
        self.assertEqual(ctx.table, 'tableName')
        self.assertEqual(ctx.index.name, 'indexName')
        self.assertEqual(len(ctx.index.columns), 1)
        self.assertEqual(ctx.index.columns[0], 'colName')


    def testCanParseTableWithColumns(self):
        example = """
        table tableName
        index indexName (colA)
        column colA int
        column colB string
        """
        ctx = self.sut(example)
        self.assertEqual(len(ctx.columns), 2)
        self.assertEqual(ctx.columns[0].name, 'colA')
        self.assertEqual(ctx.columns[0].datatype, 'int')
        self.assertEqual(ctx.columns[1].name, 'colB')
        self.assertEqual(ctx.columns[1].datatype, 'string')


    def testCanParseOptionalColumns(self):
        example = """
        table tableName
        column colA int
        column colB string optional
        column colC bool
        """
        ctx = self.sut(example)
        self.assertEqual(len(ctx.columns), 3)
        self.assertEqual(ctx.columns[0].name, 'colA')
        self.assertEqual(ctx.columns[0].datatype, 'int')
        self.assertFalse(ctx.columns[0].is_optional)
        self.assertEqual(ctx.columns[1].name, 'colB')
        self.assertEqual(ctx.columns[1].datatype, 'string')
        self.assertTrue(ctx.columns[1].is_optional)
        self.assertEqual(ctx.columns[2].name, 'colC')
        self.assertEqual(ctx.columns[2].datatype, 'bool')
        self.assertFalse(ctx.columns[2].is_optional)


    def testCanParseConstColumns(self):
        example = """
        table tableName
        column colA int
        column colB string const
        column colC bool
        """
        ctx = self.sut(example)
        self.assertEqual(len(ctx.columns), 3)
        self.assertEqual(ctx.columns[0].name, 'colA')
        self.assertEqual(ctx.columns[0].datatype, 'int')
        self.assertFalse(ctx.columns[0].is_const)
        self.assertEqual(ctx.columns[1].name, 'colB')
        self.assertEqual(ctx.columns[1].datatype, 'string')
        self.assertTrue(ctx.columns[1].is_const)
        self.assertEqual(ctx.columns[2].name, 'colC')
        self.assertEqual(ctx.columns[2].datatype, 'bool')
        self.assertFalse(ctx.columns[2].is_const)


    def testCanParseConstAndOptionalColumns(self):
        example = """
        table tableName
        column colA int
        column colB string const optional
        column colC bool optional const
        """
        ctx = self.sut(example)
        self.assertEqual(len(ctx.columns), 3)
        self.assertFalse(ctx.columns[0].is_const)
        self.assertFalse(ctx.columns[0].is_optional)
        self.assertTrue(ctx.columns[1].is_const)
        self.assertTrue(ctx.columns[1].is_optional)
        self.assertTrue(ctx.columns[2].is_const)
        self.assertTrue(ctx.columns[2].is_optional)
