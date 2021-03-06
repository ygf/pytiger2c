# -*- coding: utf-8 -*-

"""
Clase C{UnaryOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.operatornode import OperatorNode


class UnaryOperatorNode(OperatorNode):
    """
    Clase C{UnaryOperatorNode} del árbol de sintáxis abstracta.
    
    Esta clase es la clase base de todos los nodos del árbol de sintáxis
    abstracta que representan operadores unarios de Tiger.
    """
    
    def _get_expression(self):
        """
        Método para obtener el valor de la propiedad C{expression}.
        """
        return self._expression
    
    expression = property(_get_expression)
    
    def __init__(self, expression):
        """
        Inicializa la clase C{UnaryOperatorNode}.
        
        @type expression: C{LanguageNode}
        @param expression: Nodo del árbol de sintáxis abstracta representando
            la expresión a la que se va a aplicar el operador unario.
        """
        super(UnaryOperatorNode, self).__init__()
        self._expression = expression

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        expression = self.expression.generate_dot(generator)
        generator.add_edge(me, expression)
        return me
