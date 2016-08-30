#!/usr/bin/env python
# -*- coding:utf-8 -*-

from mongodb import get_item_k_code
from formula import Formula
import re

TEXT_MODE = 0
MATH_MODE = 1
UNCOMMAND = 0
COMMAND = 1
BEGIN_MATH = '[[math]]'
END_MATH = '[[/math]]'
USED = 1
UNUSED = 0
LEFT_DELIMITER = ['(', '[', '{', '\{']
RIGHT_DELIMITER = [')', ']', '}', '\}']
DELIMITERS = LEFT_DELIMITER + RIGHT_DELIMITER
MATH_BEGIN = [u'\\(', u'\\[']
MATH_END = [u'\\)', u'\\]']

escape_list = [u' ', u'#', u'$', u'%', u'^', u'&', u'(', u')', u'[', u']', u'{', u'}']
fun_parameter_map = {u'\\frac': 2, u'\\sqrt': 2, u'_': 1}

fractions = [u'\\dfrac', u'\\sfrac', u'\\cfrac', u'\\frac']


class ItemFormulae(Formula):
    def __init__(self, item_id):
        Formula.__init__(self)
        self.item_keys = {'desc', 'ans', 'exp'}
        self.item_k_code = get_item_k_code(item_id)
        self.math = {}
        self.ltx_str = ''

    def transfer_k_code(self):
        result = dict()
        for key in self.item_keys:
            k_code = self.item_k_code.get(key)
            char_list = char_list_generate(k_code)
            expr = normalize_latex(char_list)
            result[key] = expr[8:].split('[[math]]')
        self.math = result

    def set_vars_value(self):
        for key in self.var_patterns.keys():
            pattern = re.compile(self.var_patterns[key])
            for string in self.math['ans'] + self.math['exp'] + self.math['desc']:
                cnt = len(re.findall(pattern, string))
                self.vars_value[key] += cnt


def normalize_k_code(char):
    for f in fractions:
        char = char.replace(f, u'\\frac')
    char = re.sub(ur'\\sqrt(?!\s?\[)', '\\sqrt[2]', char)
    char = char.replace(ur'\right.', ur'\right}')
    char = char.replace(ur'\right}', ur'\}')
    char = char.replace(ur'\left{', ur'\{')
    char = char.replace(ur'\left', ur'')
    char = char.replace(ur'\right', ur'')
    char = char.replace(ur'\style{font-family:Times New Roman}{g}', u' ')
    return char


def normalize_parameter(par):
    if par == '':
        return par
    else:
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
                yield mode, a # 输出非控制序列的字符
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


def char_list_generate(k_code):
    char_list = []
    level = int()
    k_code = normalize_k_code(k_code)
    result = character_estimate(k_code)
    while 1:
        try:
            mode, char = result.next()
            if mode:
                if char in LEFT_DELIMITER: level += 1
                if char in RIGHT_DELIMITER: level -= 1
                char_list.append({'level': level, 'char': char, 'used': UNUSED})
        except:
            break
    return char_list


def normalize_latex(char_list, ini_level=0, idx=0, par_buffer=str()):
    length = len(char_list)
    expr = str()
    par_num = 0
    for i in xrange(idx, length):
        char, level= char_list[i].get('char'), char_list[i].get('level')
        if char_list[i]['used']:
            continue
        if level == ini_level:
            if char in fun_parameter_map.keys():
                par_num += fun_parameter_map[char]
                expr += char
            else:
                if par_num == 0:
                    expr += char
                else:
                    expr += normalize_parameter(char)
                    par_num += -1
            char_list[i]['used'] = USED
        elif level > ini_level:
            if par_num == 0:
                expr += normalize_latex(char_list, level, i, par_buffer)
            else:
                expr += normalize_parameter(normalize_latex(char_list, level, i, par_buffer))
                par_num += -1
        else:
            expr += char
            char_list[i]['used'] = USED
            return expr
    return expr