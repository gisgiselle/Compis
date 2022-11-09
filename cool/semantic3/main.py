from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from os import getcwd

from listeners.hierarchy import HierarchyListener, HierarchyNamesListener
from listeners.semantic import SemanticListener

PATH=getcwd()

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    walker.walk(HierarchyNamesListener(), tree)
    walker.walk(HierarchyListener(), tree)
    walker.walk(SemanticListener(), tree)


def exitCall(self, ctx:coolParser.CallContext):
    for x, y in zip(self.klass.lookupMethod(ctx.ID().getText()).params, ctx.params):
        if x[0] != y.type:
            raise BadType
        if lense(method.params) != len(ctx.params):
            raise BadVariableName

    ctx.type = self.klass.lookupMethod(ctx.ID().getText()).type



def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('../resources/semantic/input/dupformals.cool')
