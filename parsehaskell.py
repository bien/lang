import traceback

tokens = ('NAME', 'NUMBER', 'SCONST',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE', "MOD",
          'EQUALS', 'NOTEQUAL', 'LT', 'LTE', "GT", "GTE",
          'ASSIGN', 'ARROW',
          "AND", "OR", 
          "LPAREN", "RPAREN", "LAMBDA")

t_NAME = r"[a-zA-Z_][a-zA-Z0-9_']*"
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
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

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
    ('left', 'PLUS', "MINUS"),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
)

start = 'stmt'

def p_infix_operator(t):
    '''infix : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MOD
    | EQUALS 
    | NOTEQUAL
    | LT
    | LTE
    | GT
    | GTE
    | AND
    | OR'''
    t[0] = t[1]

def p_expr_infix(t):
   'expr : expr infix expr'
   t[0] = ((t[2], t[1]), t[3])

def p_expr_atom(t):
    '''expr : NUMBER
    | NAME
    | SCONST'''
    t[0] = t[1]

def p_expr_paren(t):
    '''expr : LPAREN expr RPAREN'''
    t[0] = t[2]

def p_expr_apply(t):
    '''expr : expr expr'''
    t[0] = ('apply', t[1], t[2])

def p_params_single(t):
    '''params : NAME'''
    t[0] = [t[1]]

def p_params_mult(t):
    '''params : params NAME'''
    t[0] = t[1]
    t[0].append(t[1])

def p_expr_lambda(t):
    '''expr : LAMBDA params ARROW expr'''
    t[0] = ('lambda', t[2], t[4])

def p_assign(t):
    '''stmt : NAME params ASSIGN expr'''
    t[0] = ('bind', t[1], ('lambda', t[2], t[4]))

def p_eval_loop(t):
    '''stmt : expr'''
    t[0] = t[1]

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

