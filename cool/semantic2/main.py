from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from os import getcwd

from listeners.semantic import SemanticListener

PATH=getcwd()

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    walker.walk(SemanticListener(), tree)


def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('../resources/semantic/input/outofscope.cool')
