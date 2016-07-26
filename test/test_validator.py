from pyscr.frontend import Validator
import unittest

class TestValidator(unittest.TestCase):
    class Mapper(object):
        def __init__(self, **args):
            for key,value in args.items():
                setattr(self, key, value)


    def setUp(self):
        self.sut = Validator()


    def testCanValidateColumnNameUniqness(self):
        colA = TestValidator.Mapper(name='colA')
        example = TestValidator.Mapper(columns=[colA])
        self.assertTrue(self.sut(example))
        example = TestValidator.Mapper(columns=[colA, colA])
        self.assertRaises(Validator.NonUniqueColumnNames, self.sut, example)
