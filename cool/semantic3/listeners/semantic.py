from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import lookupClass, SymbolTableWithScopes

'''
4. BAD ARGS1
class Main { main() : Object {0}; };

class A {
      bar() : Object {
	    (new B).foo(self, 29)
      };
};

class B inherits A {
      foo(b:B, x:Int) : String { "moo" };
};

'''

'''
5. BAD DISPTACH 
class Main { main() : Object {0}; };

class Animal {};

class Cow inherits Animal {
      moo() : String { "moo" };
};
      
class Blerg {
      foo() : Object {
	    let cow : Animal <- new Cow 
	    in cow.moo()
      };
};



'''
class SemanticListener(coolListener):
    def __init__(self):
        self.main = False

    def exitAttribute(self, ctx: coolParser.AttributeContext):
        #test_anattributenamedself
        if ctx.ID().getText() == 'self':
            raise BadAttributeName()

        #test_assignmentnoconform

    def enterKlass(self, ctx: coolParser.KlassContext):
        #test_nomain
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

        #test_badredefineint. test_redefinedobject, test_selftyperedeclared
        if ctx.TYPE(0).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE', 'Object']:
            raise BadClassName()

        #En este momento la clase ya debe estar definida, la tomo de la tabla
        self.klass = lookupClass(ctx.TYPE(0).getText())

        #Crear el scope de variables, se asocia a la klass para buscar también en atributos
        self.scopes = SymbolTableWithScopes(self.klass)

    def enterMethod(self, ctx:coolParser.MethodContext):
        #Abro el scope para variables-parámteros
        self.scopes.openScope()

    def exitMethod(self, ctx:coolParser.MethodContext):
        #Cierro el scope de parámetros
        self.scopes.closeScope()

        #test_selftypebadreturn

    def enterFormal(self, ctx: coolParser.FormalContext):
        #test_selfinformalparameter
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        #test_selftypeparameterposition
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise BadClassName()

        #test_dupformals
        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def enterLet(self, ctx:coolParser.LetContext):
        #Abro el scope de variables locales en el let
        self.scopes.openScope()

    def exitLet(self, ctx:coolParser.LetContext):
        #Cierro el scope de variables locales en el let
        #BUG: deberían ir anidadas, pero me parece en esta etapa no hay pruebas así
        #Ejemplo: let x:Int <-5, y:Int <- x in x + y;
        self.scopes.closeScope()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        #test_letself
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def exitLet_decl(self, ctx:coolParser.Let_declContext):
        #test_letbadinit
        pass

    def exitProgram(self, ctx: coolParser.ProgramContext):
        #test_nomain
        if not self.main:
            raise NoMain()

    def enterAssign(self, ctx: coolParser.AssignContext):
        #test_selfassignment
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

    # Base para el algoritmo bottom-up
    def enterInt(self, ctx:coolParser.IntContext):
        ctx.type = lookupClass('Int')

    def exitPri(self, ctx:coolParser.PriContext):
        #¡Este paso es necesario porque en la gramática hay una regla que consolida todas las literales!
        #Es necesario para darles la misma precedencia
        #Descomentar la siguiente línea una vez que los nodos de la regla primary ya tengan tipo
        #ctx.type = ctx.primary().type
        pass

    def exitAdd(self, ctx:coolParser.AddContext):
        #test_badarith
        pass

    def exitCall(self, ctx:coolParser.CallContext):
        #test_badmethodcallitself
        pass

    def exitCallobj(self, ctx:coolParser.CallobjContext):
        #test_baddispatch, test_badwhilebody, test_badargs1
        pass

    def exitCallstat(self, ctx:coolParser.CallstatContext):
        #test_badstaticdispatch, test_tricyatdispatch2
        pass

    def exitEq(self, ctx:coolParser.EqContext):
        #test_badequalitytest, test_badequalitytest2
        pass

    def exitWhile(self, ctx:coolParser.WhileContext):
        #test_badwhilecond
        pass

    def exitCase(self, ctx:coolParser.CaseContext):
        #test_caseidenticalbranch
        pass

    def exitVar(self, ctx:coolParser.VarContext):
        #test_outofscope
        pass

    def exitNew(self, ctx:coolParser.NewContext):
        #test_returntypenoexist
        pass

    def exitAssign(self, ctx:coolParser.AssignContext):
        #test_assignoconform
        pass

    def exitIf(self, ctx:coolParser.IfContext):
        #test_lubtest
        pass