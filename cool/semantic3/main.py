from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from os import getcwd

from listeners.hierarchy import HierarchyListener, HierarchyNamesListener
from listeners.semantic import SemanticListener
from util.exceptions import BadVariableName, BadType
from util.structure import lookupClass

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

#new parents id var integey primary
def enterVar(self,ctx:coolParser.VarContext):
    try:
        if ctx.ID().getText() == 'self':
            ctx.type = self.klass
        else:
            ctx.type = self.scopes[ctx.ID().getText()]
    except KeyError:
        raise

def exitPri(self, ctx:coolParser.PriContext):
    ctx.type = ctx.primary().type

def exitCallObj(self, ctx:coolParser.CallobjContext):

    for x, y in zip(self.klass.lookupMethod(ctx.ID().getText()).params, ctx.params):
    #x trae el nombre del param
        lookupClass(x.value)
        y.typeS

    if not lookupClass(x.value).conforms(y.type):
        raise BadType

    ctx.type =  ctx.expr(0).type.lookupMethod(ctx.ID().getText()).type

    pass

def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('../resources/semantic/input/dupformals.cool')
