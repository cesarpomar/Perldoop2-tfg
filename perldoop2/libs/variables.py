# -*- coding: utf-8 -*-

#Copyright 2016 César Pomar <cesarpomar18@gmail.com>
#
#This file is part of Perldoop.
#
#Perldoop is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Perldoop is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Perldoop.  If not, see <http://www.gnu.org/licenses/>.

from libs import DataType as Dtp
from libs import Variable
from libs import Type
from libs import Position


class Variables:
    
    reserved_var = {
    # Reservadas por perl
    'ARGV':0,
    '_':0,
    # Reservadas por perldoop
    'pd_argv':0,  # Argumento funciones
    'pd_me':0,  # Multi equals
    # Reservadas por java
    'abstract':0,
    'continue':0,
    'for':0,
    'new':0,
    'switch':0,
    'assert':0,
    'default':0,
    'goto':0,
    'package':0,
    'synchronized':0,
    'boolean':0,
    'do':0,
    'if':0,
    'private':0,
    'this':0,
    'break':0,
    'double':0,
    'implements':0,
    'protected':0,
    'throw':0,
    'byte':0,
    'else':0,
    'import':0,
    'public':0,
    'throws':0,
    'case':0,
    'enum':0,
    'instanceof':0,
    'return':0,
    'transient':0,
    'catch':0,
    'extends':0,
    'int':0,
    'short':0,
    'try':0,
    'char':0,
    'final':0,
    'interface':0,
    'static':0,
    'void':0,
    'class':0,
    'finally':0,
    'long':0,
    'strictfp':0,
    'volatile':0,
    'const':0,
    'float':0,
    'native':0,
    'super':0,
    'while':0,
    # Reservadas por hadoop
    'pd_key':0,
    'pd_value':0,
    'pd_context':0,
    }
    
    # Paquetes disponibles
    packages = {}
    
    # Imports disponibles
    imports_path = {
    'List':'java.util.List',
    'Map':'java.util.Map',
    'Iterator':'java.util.Iterator',
    'Mapper':'org.apache.hadoop.mapreduce.Mapper',
    'Reducer':'org.apache.hadoop.mapreduce.Reducer',
    'HadoopIO':'org.apache.hadoop.io.*',
    'HadoopContext':'org.apache.hadoop.mapreduce.Mapper.Context',
    'IOException':'java.io.IOException'
    }
    
    # Inicializa las variables globales
    @classmethod
    def global_vars(Var, parser):
        variables = dict()
        if parser.main_class:
            variables['ARGV'] = Variable(type=[Type(Dtp.ARRAY), Dtp.STRING], assign=True, name='ARGV', pos=Position())
        return [variables]
    
    # Comprueba si una variable ha sido asignada, pudiendo ignorar los atributos
    @classmethod
    def is_assign(Var, parser, var, atribute=False):
        if len(parser.assigns) > 1 or atribute:
            for level in parser.assigns:
                if var in level:
                    return True
            return False
        else:
            return True
    
    # Comprueba si la palabra esta reservada
    @classmethod
    def is_reserver(Var, parser, var):
        return var in Var.reserved_var or var in parser.reserved_var or var[:4] == 'pd_i' or var[:4] == 'pd_f'
    
    # Retorno la siguiente variable disponible para loops
    @classmethod
    def get_loop_var(Var, parser):
        return Var.calculate_var(parser, 'pd_i')
    
    # Retorno la siguiente variable disponible para funciones
    @classmethod
    def get_function_var(Var, parser):
        return Var.calculate_var(parser, 'pd_f')
    
    # Calcula una variable reservada para loops o funciones 
    @classmethod
    def calculate_var(Var, parser, var):
        # Si la raiz no esta cogida la usamos
        if var not in parser.reserved_var:
            parser.reserved_var[var] = 0
            return var
        n = 0;
        # Si no vamos añadiendo numeros hasta encontrar una libre
        while(True):
            n += 1
            var_n = var + str(n)
            if var_n not in parser.reserved_var:
                parser.reserved_var[var_n] = 0
                return var_n    
    
    # Inicializa los argumentos de las funciones   
    @classmethod
    def function_vars(Var, parser, function):
        parser.variables[-1]['_'] = Variable(type=[Dtp.VOID], name='pd_argv', pos=function.pos, multi_type=function.args[:])
        parser.assigns[-1]['pd_argv'] = True
        parser.reserved_var = {}
        
    
    # Obtiene la entrada de una variable si existe
    @classmethod
    def get_var(Var, parser, name):
        for level in range(1, len(parser.variables) + 1):
            if name in parser.variables[-level]:
                return parser.variables[-level][name]
    
    # Verifica si una variable existe en el contexto actual (global o local)
    @classmethod
    def var_exist(Var, parser, name):
        if len(parser.variables) == 1:
            return name in parser.variables[0]
        else:
            for level in range(1, len(parser.variables)):
                if name in parser.variables[-level]:
                    return True
        return False
