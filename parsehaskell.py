import traceback

reserved = { 'let': 'LET' }

tokens = ['NAME', 'NUMBER', 'SCONST',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE', "MOD",
          'EQUALS', 'NOTEQUAL', 'LT', 'LTE', "GT", "GTE",
          'ASSIGN', 'ARROW',
          "AND", "OR", 
          "TYPE",
          "LPAREN", "RPAREN", "LAMBDA"] + reserved.values()

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_EQUALS = r'=='
t_NOTEQUAL = r'[/!]='
t_LT = r"<"
t_LTE = r"<="
t_GT = r">"
t_GTE = r">="
t_AND = r"&&"
t_OR = r"\|\|"
t_ARROW = r"->"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LAMBDA = r"\\"
t_ASSIGN = r"="
t_TYPE = r"::"
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z0-9_']*"
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    raise Exception

precedence = (
    ('nonassoc', 'TYPE'),
    ('right', 'ARROW'),
    ('right', "OR"),
    ('right', 'AND'),
    ('nonassoc', 'EQUALS', 'NOTEQUAL', 'GT', "GTE", "LT", "LTE"),
    ('left', 'PLUS', "MINUS"),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'APPLY'),
)

start = 'decl'


def p_expr_infix(t):
   '''expr : expr PLUS expr
   | expr MINUS expr
   | expr TIMES expr
   | expr DIVIDE expr
   | expr MOD expr
   | expr EQUALS expr
   | expr NOTEQUAL expr
   | expr LT expr
   | expr LTE expr
   | expr GT expr
   | expr GTE expr
   | expr AND expr
   | expr OR expr'''
   t[0] = ((t[2], t[1]), t[3])

def p_expr_atom(t):
    '''expr : atom'''
    t[0] = t[1]

def p_atom(t):
    '''atom : NUMBER
    | NAME
    | SCONST'''
    t[0] = t[1]

def p_expr_paren(t):
    '''atom : LPAREN expr RPAREN'''
    t[0] = t[2]

def p_expr_apply(t):
    '''expr : expr expr %prec APPLY'''
    t[0] = ('apply', t[1], t[2])

def p_params_single(t):
    '''params : atom'''
    t[0] = [t[1]]

def p_params_mult(t):
    '''params : atom params'''
    t[0] = t[2]
    t[0].append(t[1])

def p_expr_lambda(t):
    '''expr : LPAREN LAMBDA params ARROW expr RPAREN'''
    t[0] = ('lambda', t[2], t[4])

def p_type_name(t):
    '''type : NAME'''
    t[0] = t[1]

def p_type_paren(t):
    '''type : LPAREN type RPAREN'''
    t[0] = t[2]

def p_type_func(t):
    '''type : type ARROW type'''
    t[0] = ('apply', t[1], t[3])

def p_expr_type(t):
    '''expr : expr TYPE type'''
    t[0] = ('type', t[1], t[3])

def p_assign(t):
    '''interactive : LET NAME params ASSIGN expr'''
    t[0] = ('bind', t[2], ('lambda', t[3], t[5]))

def p_eval_loop(t):
    '''interactive : expr'''
    t[0] = t[1]

def p_decl_defun(t):
    '''decl : NAME params ASSIGN expr'''
    t[0] = ('bind', t[1], ('lambda', t[2], t[4]))

def p_decl_type(t):
    '''decl : NAME TYPE type'''
    t[0] = ('type', t[1], t[3])

def p_error(t):
    print "Syntax error at '%s'" % t.value

def evalloop(input):
    import ply.lex as lex
    lex.lex()
    import ply.yacc as yacc
    yacc.yacc()
    for line in input:
        try:
            yield yacc.parse(line)
        except:
            traceback.print_exc()
            yield ''

def readstdin():
    while True:
        try:
            yield raw_input('> ')
        except EOFError:
            break

def main():
    import sys
    for e in evalloop(readstdin()):
        print e
    
if __name__ == '__main__':
    main()

