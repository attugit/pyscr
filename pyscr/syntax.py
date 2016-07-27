from . import Table, Column


class SyntaxCheckError(Exception):

    def __init__(self, msg): self.message = msg

    def __str__(self): return str(self.message)


class NonUniqueColumnNames(SyntaxCheckError):

    def __init__(self, msg):
        super(NonUniqueColumnNames, self).__init__(
            'multiple definitions of %s!' % str(msg))


class Validate(object):

    @staticmethod
    def tableName(ctx):
        return str(ctx.table)

    @staticmethod
    def getColumns(ctx):
        names = tuple(map(lambda x: x.name, ctx.columns))
        duplicates = [d for d in names if names.count(d) > 1]
        if duplicates:
            raise NonUniqueColumnNames(','.join(set(duplicates)))
        return [Column(name=col.name,
                       datatype=col.datatype,
                       is_optional=col.is_optional,
                       is_const=col.is_const) for col in ctx.columns]


class Syntax(object):

    def __call__(self, ctx):

        return Table(name=Validate.tableName(ctx), columns=Validate.getColumns(ctx))
