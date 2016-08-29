#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14
from mongodb import get_item_stem
import re

TEXT_MODE = 0
MATH_MODE = 1
UNCOMMAND = 0
COMMAND = 1
BEGIN_MATH = '[[math]]'
END_MATH = '[[/math]]'
CTRL_SQUENCE = 1
NORMAL_TEXT = 0
LEFT_DELIMITER = ['(', '[', '{', '\{']
RIGHT_DELIMITER = [')', ']', '}', '\}']
DELIMITERS = LEFT_DELIMITER + RIGHT_DELIMITER
MATH_BEGIN = [u'\\(', u'\\[']
MATH_END = [u'\\)', u'\\]']

escape_list = [u' ', u'#', u'$', u'%', u'^', u'&', u'(', u')', u'[', u']', u'{', u'}']
parameter_map = {u'\\frac': 2, u'\\sqrt': 2, u'_': 1}


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


def nomalize_latex(char):
    fractions = [u'\\dfrac', u'\\sfrac', u'\\cfrac', u'\\frac']
    for f in fractions:
        char = char.replace(f, u'\\frac')
    char = re.sub(ur'\\sqrt(?!\s?\[)', '\\sqrt[2]', char)
    char = char.replace(ur'\right.', ur'\right}')
    char = char.replace(ur'\right', u'\\')
    char = char.replace(ur'\left', u'\\')
    return char


def nomalize_parameter(par):
    if par[0] in [u'[', u'{'] and par[-1] in [u']', u'}']:
        result = par
    else:
        result = u'{' + par + u'}'
    return result


def character_estimate(latex_str):
    """ LaTeX 字处理, 将含 k_code 公式字符串中的字符提取出来, 提取粒度为单个有效控制序列 """
    mode = TEXT_MODE
    cmd = UNCOMMAND
    char_buffer = '\\'
    length = len(latex_str)
    for i in range(length):
        a = latex_str[i]
        try:
            b = latex_str[i + 1]
        except:
            b = ''
        if not cmd:
            if a == '\\':
                cmd = COMMAND
            elif a != ' ':
                yield mode, a  # 输出非控制序列的字符
        else:
            if a.isalpha():
                char_buffer += a
                if not b.isalpha():
                    char, char_buffer, cmd = char_buffer, '\\', UNCOMMAND
                    yield mode, char
            else:  # 直接转义的 LaTeX 符号
                cmd = UNCOMMAND
                if a in [u'(', u'[']:
                    mode = MATH_MODE
                    yield mode, BEGIN_MATH
                elif a in [u')', u']']:
                    mode = TEXT_MODE
                    yield mode, END_MATH
                else:  # 处理非字母符号转义 兼容\1 \2 等非法字符 待优化
                    yield mode, '\\' + a


def formula_generate(a):
    level = int()
    a = nomalize_latex(a)
    result = character_estimate(a)
    formula = Formula()
    while 1:
        try:
            mode, char = result.next()
            if mode:
                if char in LEFT_DELIMITER: level += 1
                if char in RIGHT_DELIMITER: level -= 1
                formula.chars.append({'level': level, 'char': char})
        except:
            break
    return formula


def function(chars, ini_level, idx, exprs=list(), par_buffer=str(), expr_buffer=str()):
    style = NORMAL_TEXT
    par_level = ini_level
    par_num = 0
    length = len(chars)
    if idx == length:
        return exprs
    else:
        for i in xrange(idx, length):
            char, level = chars[i].get('char'), chars[i].get('level')
            if level == ini_level:
                if style:
                    par_buffer += char
                    if level == par_level:
                        par_num -= 1
                        expr_buffer += nomalize_parameter(par_buffer)
                        par_buffer = ''
                    if par_num == 0:
                        exprs.append(expr_buffer)
                        style, expr_buffer = NORMAL_TEXT, ''
                elif char in parameter_map.keys():
                    par_num = parameter_map[char]
                    par_level = level
                    expr_buffer += char
                    style = CTRL_SQUENCE
                else:
                    exprs.append(char)
            elif level > par_level:
                function(chars, level, i, exprs, par_buffer, expr_buffer)
            else:
                return exprs

def main():
    # main_test()
    # latex_transfor_test()
    # a = get_item_stem('55de7a205417d14d2d0866d8')
    # print a
    a = ur'\(\frac{\frac{1}{2}}{3}\)'
    # a = ur'\( x_1 = x_0 + v_0t + \dfrac12a\sin\theta t^2 \) '
    # a = ur'中文\(\frac\alpha {1+{x^2}+{y^3}} 1 + 2 = \sqrt[2]3 \sqrt3 \sqrt 5 \) \(1 = \left{ 1\right.2\)A'
    # a = ur'\(\dfrac{1}{\frac a{b}}\)'
    formula = formula_generate(a)
    print function(formula.chars, 0, 0)


if __name__ == '__main__':
    main()