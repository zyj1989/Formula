#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14

TEXT_MODE = 0
MATH_MODE = 1
ORDINARY = 10
UNCOMMAND = 0
COMMAND = 1
UNESCAPE = 0
ESCAPE = 1
SCRIPT = 1
UNSCRIPT = 0
FRACTION = 1
UNFRACTION = 0

LEFT_DELIMITER = ['(', '[', '{']
RIGHT_DELIMITER = [')', ']', '}']
DELIMITERS = LEFT_DELIMITER + RIGHT_DELIMITER
MATH_BEGIN = [u'\\(', u'\\[']
MATH_END = [u'\\)', u'\\]']


class Formula(object):
    def __init__(self):
        self.chars = list()
        self.exprs = list()
        self.contents = list()

    def generate_exprs(self):
        expr_buffer = ''
        for content in self.contents:
            if content == '=':
                self.exprs.append(expr_buffer)
                expr_buffer = ''
            else:
                expr_buffer += content
        self.exprs.append(expr_buffer)


def character_estimate(latex_str, i):
    escape = UNESCAPE
    mode = TEXT_MODE
    cmd = 0
    ct_buffer = ''
    length = len(latex_str)
    escape_list = [u' ', u'#', u'$', u'%', u'^', u'&', u'(', u')', u'[', u']', u'{', u'}']
    for i in xrange(i, length):
        c = latex_str[i]
        if not escape:
            if c == '\\':
                escape = ESCAPE
                cs_begin = i
            elif c != ' ':
                yield mode, c
        else:
            if cmd: # LaTeX 控制序列
                if not c.isalpha():
                    cmd = UNCOMMAND
                    # cs_end = i if c != ' ' else i + 1 # LaTeX 控制序列后的紧接的空格属于控制序列的一部分
                    cs = latex_str[cs_begin: i]
                    escape = UNESCAPE
                    yield mode, cs
                    if c == '\\':
                        escape = ESCAPE
                        cs_begin = i

                    elif c != ' ':
                        yield mode, c
            elif c.isalpha():
                cmd = COMMAND
            else: # 直接转义的 LaTeX 符号
                if c in [u'(', u'[']:
                    mode = MATH_MODE
                    yield mode, latex_str[cs_begin: i + 1]
                elif c in [u')', u']']:
                    yield mode, latex_str[cs_begin: i + 1]
                    mode = TEXT_MODE
                else:
                    yield mode, latex_str[cs_begin: i + 1]
                escape = UNESCAPE

def formula_generate(a):

    fractions = [u'\\dfrac', u'\\sfrac', u'\\cfrac', u'\\frac']
    cs_end = 0
    level = int()
    current_level = int()
    result = character_estimate(a, cs_end)
    char_buffer = str()
    formulae = []
    formula = Formula()
    while 1:
        try:
            mode, cs = result.next()
            if mode:
                if cs in RIGHT_DELIMITER: level -= 1
                formula.chars.append({'level': level, 'char': cs})
                print mode, level, cs
                if cs in LEFT_DELIMITER: level += 1
        except:
            break
    char = str()
    print formula.chars
    sub_script = UNSCRIPT
    script_lvl = 0
    fraction = UNFRACTION
    frac_lvl = 0
    frac_series = 0
    frac_buffer = ''
    numerator = ''
    denominator = ''
    for ele in formula.chars:
        print ele
        level = ele.get('level')
        char = ele.get('char')
        if sub_script:
            if char == u'{':
                script_lvl += 1
            if char == u'}':
                script_lvl -= 1
            if script_lvl == 0:
                sub_script = UNSCRIPT
        if fraction:
            if frac_lvl == 0:
                if frac_buffer != '':
                    if frac_series == 0:
                        numerator = frac_buffer
                        frac_buffer = ''
                        frac_series += 1
                    else:
                        denominator = frac_buffer
                        frac_buffer = ''
                        char_buffer = u'\\frac{%s}{%s}' % (numerator, denominator)
                        numerator, denominator = '', ''
                        frac_series = 0
                        formula.contents.append(char_buffer)
                        char_buffer = ''
                        fraction = UNFRACTION
                if char != u'{' and fraction:
                    frac_buffer = char
                    if frac_series == 0:
                        numerator = frac_buffer
                        frac_buffer = ''
                        frac_series += 1
                    else:
                        denominator = frac_buffer
                        frac_buffer = ''
                        char_buffer = u'\\frac{%s}{%s}' % (numerator, denominator)
                        numerator, denominator = '', ''
                        frac_series = 0
                        formula.contents.append(char_buffer)
                        char_buffer = ''
                        fraction = UNFRACTION
                else:
                    frac_lvl += 1
            else:
                if char == u'}':
                    frac_lvl -= 1
                elif char == u'{':
                    frac_lvl += 1
                else:
                    frac_buffer += char
                if frac_lvl == 0 and frac_series == 1 and frac_buffer != '':
                    denominator = frac_buffer
                    frac_buffer = ''
                    char_buffer = u'\\frac{%s}{%s}' % (numerator, denominator)
                    numerator, denominator = '', ''
                    frac_series = 0
                    formula.contents.append(char_buffer)
                    char_buffer = ''
                    fraction = UNFRACTION
            # if frac_lvl != 0:
            #     frac_buffer += char
            # if char == u'}':
            #     frac_lvl -= 1
        else:
            if char in MATH_BEGIN:
                formula = Formula()
            elif char in MATH_END:
                formulae.append(formula)
            elif char == '_':
                sub_script = SCRIPT
            elif char in fractions:
                fraction = FRACTION

            else:
                if level == 0:
                    if char in RIGHT_DELIMITER:
                        char_buffer += char
                        formula.contents.append(char_buffer)
                    elif char in LEFT_DELIMITER:
                        char_buffer = char
                    else:
                        formula.contents.append(char)
                else:
                    char_buffer += char
    print '========='
    for formula in formulae:
        print '------'
        print formula.contents
        formula.generate_exprs()
        print formula.exprs