# -*- coding: utf-8 -*-

"""
Definición de las clases correspondientes a los nodos del árbol de sintáxis abstracta. 

Todas las clases deben heredar de la clase base C{LanguageNode} e implementar 
los métodos C{check_semantics} y C{generate_code} según corresponda a la estructura 
del lenguaje que representa. 
"""

from pytiger2c.errors import SemanticError, CodeGenerationError


class LanguageNode(object):
    """
    Clase base de todas las clases correspondientes a nodos del árbol de 
    sintáxis abstracta.
    """
    
    def check_semantics(self):
        """
        Comprueba que la estructura del lenguaje Tiger representada por el nodo 
        sea correcta semánticamente.
        
        @raise SemanticError: Esta excepción se lanzará cuando se encuentre algún 
            error semántico en la estructura del lenguaje representada por el nodo.
            La excepción contendrá información acerca del error.   
        """
        raise NotImplementedError()
    
    def generate_code(self):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.
        
        @raise CodeGenerationError: Esta excepción se lanzará cuando se produzca
            algún error durante la generación del código correspondiente al nodo.,
            La excepción contendrá información acerca del error.
        """
        raise NotImplementedError()