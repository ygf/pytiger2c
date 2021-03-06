# -*- coding: utf-8 -*-

"""
Paquete principal de PyTiger2C.

PyTiger2C es una implementación de un compilador del lenguaje de programación
Tiger que genera código en lenguaje C y luego el código C resultante se compila 
para generar un ejecutable específico para una plataforma.

El código C generado será conforme al standard ISO/IEC 9899:1999, comúnmente conocido 
como C99, lo cual garantiza que pueda ser procesado por cualquier compilador de C 
que implemente dicho standard.
"""

import codecs

from pytiger2c.grammar import parser
from pytiger2c.scope import RootScope
from pytiger2c.dot import DotGenerator
from pytiger2c.code import CodeGenerator
from pytiger2c.errors import PyTiger2CError, SemanticError, CodeGenerationError


__version__ = '1.0.0'

__authors__ = (
    'Yasser González Fernández <ygonzalezfernandez@gmail.com>',
    'Ariel Hernández Amador <gnuaha7@gmail.com>',
)


def syntactic_analysis(input_fd):
    """
    Realiza análisis léxico-gráfico y sintáctico de un programa Tiger. 
    
    @type input_fd: C{file}
    @param input_fd: Descriptor de fichero del programa Tiger al cual se le debe
        realizar el análisis sintáctico.
    
    @rtype: C{LanguageNode}
    @return: Como resultado del análsis sintáctico se obtiene el árbol de sintáxis 
        abstracta correspondiente al programa Tiger recibido como argumento. El 
        árbol se retorna a través del nodo de la raíz del árbol.
    
    @raise SyntacticError: Esta excepción se lanzará si se encuentra algún error de
        sintáxis durante el análisis del programa. La excepción contendrá información
        acerca del error, como por ejemplo, la línea y/o columna donde se encontró 
        el error.
    """
    data = input_fd.read()
    ast = parser.parse(data)
    return ast


def check_semantics(ast):
    """
    Realiza comprobación semántica de un programa Tiger representado por su árbol de
    sintáxis abstracta. 
    
    @type ast: C{LanguageNode}
    @param ast: Árbol de sintáxis asbtracta correspondiente a un programa Tiger.
    
    @raise SemanticError: Esta excepción se lanzará si se encuentra un error semántico
        en el árbol de sintáxis abstracta. La excepción contendrá información
        acerca del error.
    """
    errors = []
    scope = RootScope()
    ast.check_semantics(scope, errors)
    if errors:
        raise SemanticError(errors)


def generate_code(ast, output_fd):
    """
    Realiza la generación de código.
    
    @type ast: C{LanguageNode}
    @param ast: Árbol de sintáxis asbtracta correspondiente a un programa Tiger.
    
    @type output_fd: C{file}
    @param output_fd: Descriptor de fichero del archivo donde se debe escribir el
        código resultante de la traducción del programa Tiger descrito por el árbol
        de sintáxis abstracta.
        
    @raise CodeGenerationError: Esta excepción se lanzará si se produce algún error
        durante la generación de código. La excepción contendrá información acerca
        del error.
    """
    generator = CodeGenerator()
    ast.generate_code(generator)
    generator.close()
    generator.write(output_fd)


def generate_dot(ast, output_fd):
    """
    Escribe un árbol de sintáxis abstracta correspondiente a un programa Tiger
    en un archivo con formato DOT de Graphviz.
    
    @type ast: C{LanguageNode}
    @param ast: Árbol de sintáxis asbtracta correspondiente a un programa Tiger.
    
    @type output_fd: C{file}
    @param output_fd: Descriptor de fichero del archivo donde se debe escribir el
        árbol de sintáxis abstracta en formato DOT de Graphviz.
    """
    generator = DotGenerator()
    ast.generate_dot(generator)
    generator.write(output_fd)


def tiger2dot(tiger_filename, dot_filename):
    """
    Genera un archivo en el formato DOT de Graphviz con el árbol de sintáxis
    abstracta correspondiente a un programa Tiger.
    
    Se utiliza la función auxiliar C{syntactic_analysis} para realizar el
    análisis léxico-gráfico y sintáctico durante el cual se reportará cualquier
    error en el programa Tiger. Luego, se utiliza la función auxiliar
    C{generate_dot} para escribir el árbol de sintáxis abstracta en el 
    archivo DOT.
    
    @type tiger_filename: C{str}
    @param tiger_filename: Ruta absoluta al archivo que contiene el código
        fuente del programa Tiger.
        
    @type dot_filename: C{str}
    @param dot_filename: Ruta absoluta al archivo donde se generará el archivo
        DOT resultante. Si existe un archivo en la ruta especificada este será
        sobreescrito.
    
    @raise PyTiger2CError: Además de las excepciones lanzadas por cada una de las
        funciones auxiliares, esta función puede lanzar esta excepción cuando
        se produce algún error al leer del archivo que contiene el programa
        Tiger que se quiere traducir o al escribir el árbol de sintáxis asbtracta
        resultante en el archivo DOT especificado.    
    """ 
    try:
        with codecs.open(tiger_filename, encoding='utf-8', mode='rb') as input_fd: 
            ast = syntactic_analysis(input_fd)
    except IOError:
        raise PyTiger2CError(message='Could not open the Tiger input file')
    try:
        with codecs.open(dot_filename, encoding='utf-8', mode='wb') as output_fd:
            generate_dot(ast, output_fd)
    except IOError:
        raise PyTiger2CError(error_msg='Could not open the output file')
    

def tiger2c(tiger_filename, c_filename):
    """
    Traduce un programa Tiger a un programa C equivalente.
    
    Se utiliza las funciones auxiliares C{syntactic_analysis}, C{check_semantics} 
    y C{generate_code} para llevar a cabo cada una de las fases de la compilación 
    del programa: análisis léxico-gráfico y sintáctico, comprobación semántica y
    generación de código respectivamente. Cada una de estas funciones lanzará
    las excepciones C{SyntacticError}, C{SemanticError} y C{CodeGenerationError} si
    se produce un error durante alguna de las fases. Consulte la documentación 
    de cada función para conocer los detalles.
    
    @type tiger_filename: C{str}
    @param tiger_filename: Ruta absoluta al archivo que contiene el código
        fuente del programa Tiger.

    @type c_filename: C{str}
    @param c_filename: Ruta absoluta al archivo donde se generará el código
        C resultante. Si existe un archivo en la ruta especificada este será
        sobreescrito.
        
    @raise PyTiger2CError: Además de las excepciones lanzadas por cada una de las
        funciones auxiliares, esta función puede lanzar esta excepción cuando
        se produce algún error al leer del archivo que contiene el programa
        Tiger que se quiere traducir o al escribir el código C resultante
        en el archivo especificado.
    """
    try:
        with codecs.open(tiger_filename, encoding='utf-8', mode='rb') as input_fd: 
            ast = syntactic_analysis(input_fd)
    except IOError:
        raise PyTiger2CError(message='Could not open the Tiger input file')
    check_semantics(ast)
    try:
        with codecs.open(c_filename, encoding='utf-8', mode='wb') as output_fd:
            generate_code(ast, output_fd)
    except IOError:
        raise PyTiger2CError(error_msg='Could not open the output file')
