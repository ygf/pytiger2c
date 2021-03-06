# -*- coding: utf-8 -*-

"""
Clase C{AssignmentNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class AssignmentNode(NonValuedExpressionNode):
    """
    Clase C{AssignmentNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de asignación del lenguaje Tiger. La estructura 
    de asignación tiene una expresion (lvalue) de acceso a una variable, un 
    elemento de un array o un campo de un record y un valor que se le 
    asignará a este acceso.
    """
    
    def _get_lvalue(self):
        """
        Método para obtener el valor de la propiedad C{lvalue}.
        """
        return self._lvalue
    
    lvalue = property(_get_lvalue)
    
    def _get_expression(self):
        """
        Método para obtener el valor de la propiedad C{expression}.
        """
        return self._expression
    
    expression = property(_get_expression)
    
    def __init__(self, lvalue, expression):
        """
        Inicializa la clase C{AssignmentNode}.
        
        @type lvalue: C{AccessNode}.
        @param lvalue: Expresión a la que se le quiere asignar la expresión.
        
        @type expression: C{LanguageNode}
        @param expresion: Expresión
        """
        super(AssignmentNode, self).__init__()
        self._lvalue = lvalue
        self._expression = expression

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de asignación tiene una expresion (lvalue) de acceso a una
        variable, un elemento de un array o un campo de un record y un 
        valor que se le asignará a este acceso.
        
        En la comprobación semántica de este nodo del árbol se comprueban 
        semánticamente tanto el lvalue como la expresión, luego se comprueba
        que el lvalue como la expresión retornen valor y que el tipo de retorno
        de ambos sea el mismo. Además es necesario comprobar que el lvalue no 
        es de solo lectura, pues en condiciones del lenguaje no es posible 
        modificar el valor de una variable. Se reportarán errores si se encuentran
        errores durante la comprobación semántica del lvalue o de la expresión,
        si alguno de estos no retornan tipo, si los tipos no son iguales. 
        """
        self._scope = scope
        
        errors_before = len(errors)        
        
        self.lvalue.check_semantics(self.scope, errors)
        
        if errors_before != len(errors):
            return           
        
        self.expression.check_semantics(self.scope, errors)
        
        if errors_before != len(errors):
            return        
        
        if self.lvalue.read_only:
            message = 'Invalid use of assignment to a read only variable at line {line}'
            errors.append(message.format(line=self.line_number))
        elif not self.lvalue.has_return_value():
            message = 'Invalid use of assignment to a non valued variable at line {line}'
            errors.append(message.format(line=self.line_number))
        elif not self.expression.has_return_value():
            message = 'Invalid assignment of a non valued expression at line {line}'
            errors.append(message.format(line=self.line_number))
        elif self.expression.return_type == NilType():
            if not isinstance(self.lvalue.return_type, RecordType):
                message = 'Invalid nil value of assigment at line {line}'
                errors.append(message.format(line=self.line_number))
        elif self.lvalue.return_type != self.expression.return_type:
            message = 'Incompatible types in assigment at line {line}'
            errors.append(message.format(line=self.line_number))

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        lvalue = self.lvalue.generate_dot(generator)
        expression = self.expression.generate_dot(generator)
        generator.add_edge(me, lvalue)
        generator.add_edge(me, expression)
        return me
    
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        self.lvalue.generate_code(generator)
        self.expression.generate_code(generator)
        generator.add_statement('{0} = {1};'.format(self.lvalue.code_name, 
                                                    self.expression.code_name))