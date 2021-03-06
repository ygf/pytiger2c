# -*- coding: utf-8 -*-

"""
Clase C{ForStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.variabletype import VariableType
from pytiger2c.scope import Scope


class ForStatementNode(NonValuedExpressionNode):
    """
    Clase C{ForStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{for} del lenguaje Tiger. La expresión C{for}
    evalúa las expresiones correspondientes a los límites inferiores y superiores
    y por cada valor entero entre estos valores (incluidos los extremos) evalúa
    la expresión seguida del C{do} con una variable entera con el nombre dado
    que toma el valor del entero correspondiente. La variable del índice de 
    cada iteración sólo debe ser visible para la expresión seguida de C{do}
    y es un error cambiar su valor.
    """
    
    def _get_index_name(self):
        """
        Método para obtener el valor de la propiedad C{index_name}.        
        """
        return self._index_name
    
    index_name = property(_get_index_name)
    
    def _get_lower_expression(self):
        """
        Método para obtener el valor de la propiedad C{lower_expression}.        
        """
        return self._lower_expression
    
    lower_expression = property(_get_lower_expression)
    
    def _get_upper_expression(self):
        """
        Método para obtener el valor de la propiedad C{upper_expression}.        
        """
        return self._upper_expression
        
    upper_expression = property(_get_upper_expression)
    
    def _get_expression(self):
        """
        Método para obtener el valor de la propiedad C{expression}.        
        """    
        return self._expression
    
    expression = property(_get_expression)
    
    def __init__(self, index_name, lower_expression, upper_expression, expression):
        """
        Inicializa la clase C{ForStatementNode}.
        
        @type index_name: C{str}
        @param index_name: Nombre de la variable de índice del ciclo.
        
        @type lower_expression: C{LanguageNode}
        @param lower_expression: Nodo del árbol de sintáxis abstrata
            correspondiente al límite inferior del rango para la variable
            de índice.
        
        @type upper_expression: C{LanguageNode}
        @param upper_expression: Nodo del árbol de sintáxis abstrata
            correspondiente al límite superior del rango para la variable
            de índice.
        
        @type expression: C{LanguageNode}
        @param expression: Nodo del árbol de sintáxis abstracta correspondiente
            a la expresión que se debe ejecutar para cada valor de la variable
            de índice.
        """
        super(ForStatementNode, self).__init__()
        self._index_name = index_name
        self._lower_expression = lower_expression
        self._upper_expression = upper_expression
        self._expression = expression

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
             
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se crea un nuevo ámbito que contendrá la definicion de la variable de índice
        del ciclo como sólo lectura. Este ámbito tendrá como padre el ámbito donde
        fue definido el ciclo C{for}. 
        
        Luegoo, se comprueban semánticamente las expresiones correspondientes a los
        extremos inferiores y superiores del intervalo. Estas expresiones deben 
        tener valor de retorno entero. Además se comprueba semánticamente la 
        expresión que se ejecutará en cada iteración y esta se deja libre de 
        tener o no valor de retorno.
        """
        integer_type = IntegerType()
        
        self._scope = Scope(scope)
        self.scope.define_variable(self.index_name, VariableType(integer_type, True))
        
        errors_before = len(errors)
        
        self.lower_expression.check_semantics(self.scope, errors)
        
        if errors_before == len(errors): 
            if not self.lower_expression.has_return_value(): 
                message = 'The expression for the lower bound of the for loop ' \
                          'at line {line} does not return a value'
                errors.append(message.format(line=self.line_number))
            elif self.lower_expression.return_type != integer_type:
                message = 'The return type of the expression for the lower bound ' \
                          'of the for loop at line {line} is not integer'
                errors.append(message.format(line=self.line_number))
                
        errors_before = len(errors)
            
        self.upper_expression.check_semantics(self.scope, errors)
        
        if errors_before == len(errors):
            if not self.upper_expression.has_return_value(): 
                message = 'The expression for the upper bound of the for loop ' \
                          'at line {line} does not return a value'
                errors.append(message.format(line=self.line_number))
            elif self.upper_expression.return_type != integer_type:
                message = 'The return type of the expression for the upper bound ' \
                          'of the for loop at line {line} is not integer'
                errors.append(message.format(line=self.line_number))
            
        self.expression.check_semantics(self.scope, errors)

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        index_name = generator.add_node(self.index_name)
        lower_expression = self.lower_expression.generate_dot(generator)
        upper_expression = self.upper_expression.generate_dot(generator)
        expression = self.expression.generate_dot(generator)
        generator.add_edge(me, index_name)
        generator.add_edge(me, lower_expression)
        generator.add_edge(me, upper_expression)
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
        if self.scope.parent:
            statement = '{scope}->parent = {parent};'
            statement = statement.format(scope=self.scope.code_name, 
                                         parent=self.scope.parent.code_name)
            generator.add_statement(statement)
        
        self.lower_expression.generate_code(generator)
        self.upper_expression.generate_code(generator)
        
        index_code_name = self.scope.get_variable_code(self.index_name)
        generator.add_statement('{0} = {1};'.format(index_code_name, 
                                                    self.lower_expression.code_name))
        statement = 'while({0} <= {1})'.format(index_code_name, 
                                               self._upper_expression.code_name)
        generator.add_statement(statement)
        generator.add_statement('{')
        self.expression.generate_code(generator)
        generator.add_statement('{0}++;'.format(index_code_name))
        generator.add_statement('}')
            
            