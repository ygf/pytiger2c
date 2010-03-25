# -*- coding: utf-8 -*-

"""
Clase C{ArrayLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.arraytype import ArrayType
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class ArrayLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{ArrayLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa la creación de una instancia de un tipo array definido con 
    anterioridad. La creación de una instancia de un tipo array recibe el 
    nombre del tipo de array que se quiere crear, una expresión que 
    corresponde a la cantidad de elementos que va a tener el array y por 
    último una expresión que corresponde al valor con el que se inicializarán
    todos los miembros de este nuevo array.
    """
    
    def _get_type_name(self):
        """
        Método para obtener el valor de la propiedad C{type_name}.
        """
        return self._type_name
    
    type_name = property(_get_type_name)
    
    def _get_count(self):
        """
        Método para obtener el valor de la propiedad C{count}.
        """
        return self._count
    
    count = property(_get_count)
    
    def _get_value(self):
        """
        Método para obtener el valor de la propiedad C{value}.
        """
        return self._value
    
    value = property(_get_value) 
    
    def __init__(self, type_name, count, value):
        """
        Inicializa la clase C{ArrayLiteralExpressionNode}.
        
        @type type_name: C{str}
        @param type_name: Nombre del tipo de array que se quiere crear.
        
        @type count: C{LanguageNode}
        @param count: Expresión correspondiente a la cantidad de elementos
            que se quiere crear.
            
        @type value: C{LanguageNode}
        @param value: Expresión correspondiente al valor con el que se quiere 
            inicializar los miembros del array
        """
        super(ArrayLiteralExpressionNode, self).__init__()
        self._type_name = type_name
        self._count = count
        self._value = value

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La creación de una instancia de un tipo array recibe el nombre del
        tipo de array que se quiere crear, una expresión que corresponde a 
        la cantidad de elementos que va a tener el array y por último una 
        expresión que corresponde al valor con el que se inicializarán todos 
        los miembros de este nuevo array.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueba que el tipo array que se quiere crear ha sido definido en
        el ámbito correspondiente, se comprueba que la expresión correspondiente
        a la cantidad de elementos del array tenga valor de retorno y que este
        sea entero, por último se comprueba que la expresión correspondiente al
        valor que se le asignará a cada miembro de este nuevo array retorne
        tipo y que este sea igual al correspondiente a los valores en la 
        declaración del tipo de array.        
        """
        self._scope = scope
        try:
            self._return_type = self.scope.get_type_definition(self.type_name)
        except KeyError:
            message = 'Undefined type {type_name} at line {line}'
            errors.append(message.format(type_name = self._type_name, 
                                         line=self.line_number))
        if isinstance(self.return_type, ArrayType):
            self.count.check_semantics(self.scope, errors)
            if not self.count.has_return_value():
                message = 'Non value expression for the array length at line {line}'
                errors.append(message.format(line=self.line_number))
            elif self.count.return_type != IntegerType():
                message = 'Non integer expression for the array length at line {line}'
                errors.append(message.format(line=self.line_number))
            self.value.check_semantics(self.scope, errors)
            if not self.value.has_return_value():
                message = 'Non valued expression for the array value at line {line}'
                errors.append(message.format(line=self.line_number))
            elif self.value.return_type == NilType():
                if not isinstance(self.return_type.fields_types[0], RecordType):
                    message = 'Invalid nil value for the array value at line {line}'
                    errors.append(message.format(line=self.line_number))
            elif self.value.return_type != self.return_type.fields_types[0]:
                message = 'Incompatible type for the array value at line {line}'
                errors.append(message.format(line=self.line_number))
        else:
            message = 'Invalid non array type {type_name} at line {line}'
            errors.append(message.format(type_name = self._type_name, 
                                         line=self.line_number))