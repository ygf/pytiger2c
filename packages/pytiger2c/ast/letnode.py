# -*- coding: utf-8 -*-

"""
Clase C{LetNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.scope import Scope, FakeScope


class LetNode(ValuedExpressionNode):
    """
    Clase C{LetNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{let-in-end} del lenguaje Tiger. La expresión 
    C{let-in-end} define tipos y funciones especificadas luego de la instrucción
    C{let} y antes de la instrucción C{in} de forma tal que esas declaraciones 
    estén disponibles en el ámbito de ejecución de la secuencia de expresiones 
    que se encuentran detrás de la instrucción C{in} y antes de la instrucción 
    C{end}.
    
    La expresión C{let-in-end} retorna valor si la secuencia de expresiones
    retorna valor y su tipo de retorno es el mismo que la secuencia de 
    expresiones.
    """
    
    def __init__(self, type_declaration_groups, function_declaration_groups, 
                 variable_declarations, expressions):
        """
        Inicializa la clase C{LetNode}.
        
        @type type_declaration_groups: C{list}
        @param type_declaration_groups: Lista de los grupos de las declaraciones
            de tipos, que forman parte de la lista de declaraciones de la
            estructura C{let-in-end} representada por este nodo del árbol
            de sintáxis abstracta.
            
        @type function_declaration_groups: C{list}
        @param function_declaration_groups: Lista de los grupos de las declaraciones
            de funciones, que forman parte de la lista de declaraciones de la
            estructura C{let-in-end} representada por este nodo del árbol
            de sintáxis abstracta.
        
        @type variable_declarations: C{list}
        @param variable_declarations: Lista de las declaraciones de variables 
            que forman parte de la lista de declaraciones de la
            estructura C{let-in-end} representada por este nodo del árbol
            de sintáxis abstracta.
            
        @type expressions: C{ExpressionSequenceNode}
        @param expressions: Sequencia de expresiones que forman parte del cuerpo
            de la expresión C{let-in-end} representada por este nodo del árbol
            de sintáxis abstracta.
        """
        super(LetNode, self).__init__()
        self._type_declaration_groups = type_declaration_groups
        self._function_declaration_groups = function_declaration_groups
        self._variable_declarations = variable_declarations
        self._expressions = expressions

    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.      
        """
        return self._return_type != None 

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        primeramente se crea el nuevo ámbito que define la estructura y que
        tendrá como padre el ámbito donde se define la estructura C{let-in-end}.
        
        Se recorren todos los grupos de declaraciones de tipos, definiendo los 
        tipos en el ámbito creado y se obtiene un conjunto de los tipos que se 
        declaran en cada grupo a través del método C{collect_definitions} y luego
        se comprueba semánticamente cada una de estas definiciones de tipos.
        
        Se recorren todos los grupos de declaraciones de funciones, comprobando
        la cabecera de la declaración de la función, definiendo las funciones en 
        el ámbito creado y se obtiene un conjunto de las funciones que se definen
        en cada grupo través del método C{collect_definitions}.
        
        Se comprueban semánticamente todas las declaraciones de variables.
        
        Se comprueban semánticamente los cuerpos de las funciones declaradas en
        cada grupo de declaración de funciones.
        
        Se comprueba semánticamente la secuencia de expresiones de la estructura
        C{let-in-end} y se asigna el valor de retorno del nodo, en caso de que
        lo tenga.
        
        En el procedimiento de comprobación semántica descrito anteriormente se
        realizan dos recorridos por ciertas partes del árbol de sintáxis abstracta
        descendiente de este nodo. Se recorren dos veces los nodos correspondientes
        a las declaraciones de tipos: una primera vez para obtener los nomrbes de los
        tipos que se definen en cada grupo y luego para comprobar semánticamente 
        estas declaraciones de tipos. De manera semejante, se recorren dos veces los 
        nodos del árbol de sintáxis abstracta correspondientes a las declaraciones 
        de las funciones: una primera vez para obtener los nombres de las funciones
        que se definen en cada grupo y una segunda vez para comprobar semánticamente
        el cuerpo de las funciones.
        """
        self._scope = Scope(scope)
        all_types = set()
        groups_types = []
        all_functions = set()
        groups_functions = []
        
        # First pass through the nodes of the type declarations.
        for type_declaration_group in self._type_declaration_groups:
            group_types = type_declaration_group.collect_definitions(self.scope, errors)
            groups_types.append(group_types)
            all_types.update(group_types)
            
        # Second pass through the nodes of the type declarations.
        for index, type_declaration_group in enumerate(self._type_declaration_groups):
            group_scope = FakeScope(self.scope, all_types - groups_types[index], set())
            type_declaration_group.check_semantics(group_scope, errors)
            
        # First pass through the nodes of the function declarations.
        for func_declaration_group in self._function_declaration_groups:
            group_functions = func_declaration_group.collect_definitions(self.scope, errors)
            groups_functions.append(group_functions)
            all_functions.update(group_functions)
            
        # The only pass through the nodes of the variable declarations.
        for variable_declaration in self._variable_declarations:
            variable_declaration.check_semantics(self.scope, errors)
            
        # Second pass through the nodes of the function declarations.
        for index, func_declaration_group in enumerate(self._function_declaration_groups):
            group_scope = FakeScope(self.scope, set(), all_functions - groups_functions[index])
            func_declaration_group.check_semantics(group_scope, errors)
        
        # The only pass through the expressions.
        self._expressions.check_semantics(self.scope, errors)
        
        # Setting the return value of the node.
        if self._expressions.has_return_value():
            self._return_type = self._expressions.return_type
        else:
            self._return_type = None      
