#!/usr/bin/python
# -*- coding: utf-8 -*-
import libs.ply.yacc as yacc
import libs.ply.lex as lex
import libs.Datatypes as Datatypes

def create_production(values):
    return yacc.YaccProduction([lex.LexToken()]+values)

def create_token(value,lexpos=0,lineno=0,type=None):
    token = lex.LexToken()
    token.type = type
    token.value = value
    token.lineno = lineno
    token.lexpos = lexpos
    return token

def check_position(position,lexpos=0,line=0):
    return position.lexpos == lexpos and position.line == line

def create_var(parser,name,type=None):
    context_var=parser.variables[-1]
    entry=Datatypes.Variable(name=name,type=type)
    context_var[name]=entry 
    