#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import parser.parserUtils as ParserUtils
from libs import Parser
from libs import DataType as Dtp

class TestValue(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.LINENO = 10
        self.LEXPOS = 100

    def test_p_value_int(self):
        token = ParserUtils.create_token("1", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_int(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "1", "El valor no es correcto")
        self.assertEqual(p[0].type, [Dtp.INTEGER], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta")
        
    def test_p_value_float(self):
        token = ParserUtils.create_token("1.0", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_float(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "1.0", "El valor no es correcto")
        self.assertEqual(p[0].type, [Dtp.DOUBLE], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta")    
        
    def test_p_value_string_quote(self):
        token = ParserUtils.create_token("hola mundo", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_string_quote(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "\"hola mundo\"", "El valor no es correcto")
        self.assertEqual(p[0].type, [Dtp.STRING], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta") 
        
    def test_p_value_string_double_quote(self):
        token = ParserUtils.create_token("hola mundo", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_string_double_quote(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "\"hola mundo\"", "El valor no es correcto")
        self.assertEqual(p[0].type, [Dtp.STRING], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta") 
        
    def test_p_value_cmd(self):
        token = ParserUtils.create_token("ls -l", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_cmd(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "Pd.cmd(\"ls -l\")", "El valor no es correcto")
        self.assertEqual(p[0].type, [Dtp.STRING], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta")
        # Probamos con una variable que es una cadena
        ParserUtils.create_var(self.parser, "var", [Dtp.STRING])
        token = ParserUtils.create_token("$var", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_cmd(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "Pd.cmd(var)", "La variable fue ignorada")
        self.assertEqual(p[0].type, [Dtp.STRING], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta")
        # Probamos con una variable que no es una cadena
        ParserUtils.create_var(self.parser, "var", [Dtp.INTEGER])
        token = ParserUtils.create_token("$var", self.LINENO, self.LEXPOS)
        p = ParserUtils.create_production([token])
        self.parser.p_value_cmd(p)
        self.assertIsNotNone(p[0], "La regla debe devolver un valor")
        self.assertEqual(p[0].value, "Pd.cmd(String.valueOf(var))", "La variable no fue convertida")        
        self.assertEqual(p[0].type, [Dtp.STRING], "El tipo no es correcto")
        self.assertTrue(ParserUtils.check_position(p[0].pos, self.LINENO, self.LEXPOS), "La posición no es correcta")
        