# lexer.py. This file automatically created by PLY (version 3.3). Don't edit!
_tabversion   = '3.3'
_lextokens    = {'THEN': 1, 'DO': 1, 'LBRACKET': 1, 'WHILE': 1, 'COLON': 1, 'INTLIT': 1, 'MINUS': 1, 'RBRACE': 1, 'STRLIT': 1, 'LE': 1, 'RPAREN': 1, 'SEMICOLON': 1, 'NE': 1, 'TO': 1, 'LT': 1, 'PLUS': 1, 'COMMA': 1, 'ARRAY': 1, 'ASSIGN': 1, 'FUNCTION': 1, 'GT': 1, 'END': 1, 'DIVIDE': 1, 'FOR': 1, 'PERIOD': 1, 'ELSE': 1, 'GE': 1, 'LPAREN': 1, 'IN': 1, 'VAR': 1, 'TIMES': 1, 'EQ': 1, 'ID': 1, 'IF': 1, 'AND': 1, 'LBRACE': 1, 'NIL': 1, 'OF': 1, 'BREAK': 1, 'LET': 1, 'RBRACKET': 1, 'TYPE': 1, 'OR': 1}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'COMMENT': 'exclusive', 'INITIAL': 'inclusive'}
_lexstatere   = {'COMMENT': [('(?P<t_ANY_comment_begin>/\\*)|(?P<t_COMMENT_comment_end>\\*/)|(?P<t_ANY_newline>\\r*\\n(\\r|\\n)*)', [None, ('t_ANY_comment_begin', 'comment_begin'), ('t_COMMENT_comment_end', 'comment_end'), ('t_ANY_newline', 'newline')])], 'INITIAL': [('(?P<t_ANY_comment_begin>/\\*)|(?P<t_ANY_newline>\\r*\\n(\\r|\\n)*)|(?P<t_ID>[a-zA-Z][a-zA-Z0-9_]*)|(?P<t_STRLIT>\\"((\\\\[nt])|(\\\\")|(\\\\\\\\)|(\\\\\\^[@A-Z[\\]^_])|(\\\\[0-9]{3})|(\\\\\\s+\\\\)|([^\\\\"]))*\\")|(?P<t_INTLIT>\\d+)|(?P<t_RBRACE>\\})|(?P<t_LE><=)|(?P<t_LBRACKET>\\[)|(?P<t_NE><>)|(?P<t_PLUS>\\+)|(?P<t_LPAREN>\\()|(?P<t_OR>\\|)|(?P<t_LBRACE>\\{)|(?P<t_PERIOD>\\.)|(?P<t_TIMES>\\*)|(?P<t_RBRACKET>\\])|(?P<t_GE>>=)|(?P<t_RPAREN>\\))|(?P<t_ASSIGN>:=)|(?P<t_LT><)|(?P<t_AND>&)|(?P<t_COLON>:)|(?P<t_COMMA>,)|(?P<t_EQ>=)|(?P<t_DIVIDE>/)|(?P<t_MINUS>-)|(?P<t_SEMICOLON>;)|(?P<t_GT>>)', [None, ('t_ANY_comment_begin', 'comment_begin'), ('t_ANY_newline', 'newline'), None, ('t_ID', 'ID'), ('t_STRLIT', 'STRLIT'), None, None, None, None, None, None, None, None, (None, 'INTLIT'), (None, 'RBRACE'), (None, 'LE'), (None, 'LBRACKET'), (None, 'NE'), (None, 'PLUS'), (None, 'LPAREN'), (None, 'OR'), (None, 'LBRACE'), (None, 'PERIOD'), (None, 'TIMES'), (None, 'RBRACKET'), (None, 'GE'), (None, 'RPAREN'), (None, 'ASSIGN'), (None, 'LT'), (None, 'AND'), (None, 'COLON'), (None, 'COMMA'), (None, 'EQ'), (None, 'DIVIDE'), (None, 'MINUS'), (None, 'SEMICOLON'), (None, 'GT')])]}
_lexstateignore = {'COMMENT': ' \t', 'INITIAL': ' \t'}
_lexstateerrorf = {'COMMENT': 't_COMMENT_error', 'INITIAL': 't_error'}
