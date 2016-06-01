# -*- coding: utf-8 -*-

class Called(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message
            
def fake_error(parser=None, error=None, position=None, **names):
    raise Called(error)