#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14


class Formula(object):
    """used for formula analysis"""
    def __init__(self):
        self.structure = 'ord'
    foo = 100

class Fraction(Formula):

    def __init__(self, numerator, denominator):
        Formula.__init__(self)
        assert 0 != denominator
        self.numerator = numerator
        self.denominator = denominator
        self.value = numerator / float(denominator)

print dir(Formula)
print Formula.__dict__
print Fraction.__dict__
print Fraction.__base__
print Fraction.__module__
Formula.foo = 101
c = Fraction(1, 3)
a = c
b = Formula()
c.foo = 102
print id(c)
print id(a)
print b.foo
print c.foo
print c.structure
print c.denominator
print c.numerator
print c.value
print Formula.__doc__
