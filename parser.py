#!/usr/bin/python3

tokens = (
    'WORD',#'OTHER_CHAR',
    'SPACE','NEWLINE','EQUALS','LPAREN','RPAREN',
    )

# Tokens

t_EQUALS  = r'='
t_LPAREN  = r'{'
t_RPAREN  = r'\}'
t_WORD    = r'[a-zA-Z0-9_,\.\\\/\(\)\-:;\[\]\+\-\%\@]+'
t_SPACE    = r'\ +'
#t_OTHER_CHAR    = r'[]+'

def t_NEWLINE(t):
    r'[\r\n]+'
    t.lexer.lineno += len(t.value)
    return t

# Ignored characters
t_ignore = "\t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
        ('left','EQUALS'),
        ('left','LPAREN'),
        ('left','RPAREN'),
        ('left','WORD')
    )

class KV:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __str__(self):
        return '%s:%s' % (self.key, self.value)
    def __repr__(self):
        return self.__str__()

class Node(list):
    pass

def p_space(t):
    '''equal : EQUALS
             | SPACE EQUALS
             | equal SPACE
    '''                    ## not SPACE squal for thery reason

def p_lparen(t):
    '''lparen : LPAREN
              | NEWLINE LPAREN
              | lparen NEWLINE
    '''

def p_rparen(t):
    '''rparen : RPAREN
              | NEWLINE RPAREN
              | rparen NEWLINE
    '''

def p_close_set(t):
    'kv : WORD lparen set rparen'
    t[0] = KV(t[1],t[3])
    #print('kv',t[0])

def p_close_empty_set(t):
    'kv : WORD lparen rparen'
    t[0] = KV(t[1],[])
    #print('kv',t[0])

def p_statement_assign(t):
    'kv : WORD value'
    t[0] = KV(t[1],t[2])
    #print('kv',t[0])

def p_set_assign(t):
    'set : set NEWLINE kv'
    t[1].append(t[3])
    t[0] = t[1]
    #print('set_a',t[0])

def p_value(t):
    '''value : value SPACE
             | value WORD
    '''
    t[0] = t[1] + t[2]
    #print('value',t[0])

def p_set_start(t):
    'set : kv'
    t[0] = Node()
    t[0].append(t[1])
    print('set',t[0])

def p_value_start(t):
    'value : equal'
    t[0] = ''
    #print('value',t[0])

def p_obj(t):
    'obj : set NEWLINE'   #ugly
    print('result',t[1])
    t[0] = t[1]

start = 'obj'
def p_error(t):
    if t:
        print("Syntax error on line %d pos %d type %s value '%s'" % (t.lineno, t.lexpos, t.type, t.value))
    else:
        print('perror None')

import ply.yacc as yacc
parser = yacc.yacc()

import sys 
with open(sys.argv[1]) as fd:
    text = ''.join(fd.readlines())
    '''
    lexer.input(text)
    with open("tex_dump",'w') as fd:
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok,file=fd)
'''
    parser.parse(text)
