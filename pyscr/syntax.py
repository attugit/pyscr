from . import Table, Column


class SyntaxCheckError(Exception):

    def __init__(self, msg): self.message = msg

    def __str__(self): return str(self.message)


class NoColumnsProvided(SyntaxCheckError):

    def __init__(self):
        super(NoColumnsProvided, self).__init__(
            'no column definitions provided!')


class Validate(object):

    @staticmethod
    def tableName(ctx):
        return str(ctx.table)

    @staticmethod
    def getColumns(ctx):
        if len(ctx.columns) == 0:
            raise NoColumnsProvided
        return [Column(name=col.name,
                       datatype=col.datatype,
                       is_optional=col.is_optional,
                       is_const=col.is_const) for col in ctx.columns]


class Syntax(object):

    def __call__(self, ctx):

        return Table(name=Validate.tableName(ctx), columns=Validate.getColumns(ctx))
