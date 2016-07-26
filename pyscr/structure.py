from enum import Enum


class Mapper(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class DataType(Enum):
    string = 'string'
    int = 'int'
    bool = 'bool'
    double = 'double'


class Column(Mapper):

    def __init__(self, name, datatype, is_optional=False, is_const=False):
        super(Column, self).__init__(name=str(name), datatype=DataType(datatype),
                                     is_optional=True if is_optional else False,
                                     is_const=True if is_const else False)


class Index(Mapper):

    def __init__(self, name, columns):
        super(Index, self).__init__(
            name=str(name), columns=set([str(c) for c in columns]))


class Table(Mapper):

    def __init__(self, name, columns, index=False):
        super(Table, self).__init__(name=str(name), columns=Mapper(), index=None)
        for c in columns:
            self.columns[c.name] = c
