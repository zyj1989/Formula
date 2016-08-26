#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-24 16:21

from latex2sympy.process_latex import process_sympy
from illegal_string_exception import IllegalStringException

a = u'a \\frac{1}{2}'
def latex_transfor_test(str = a):
    result = process_sympy(str)
    print result