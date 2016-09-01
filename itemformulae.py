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
func_parameter_map = {u' \\frac': 2, u' \\sqrt': 2, u'^': 1}
annihilate_map = {u'_': 1, u' \\begin': 1, u' \\end': 1}
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
            math = normalize_latex(char_list)
            result[key] = math[8:].split('[[math]]')
        self.math = result
        self.maths = self.math['ans'] + self.math['exp'] + self.math['desc']

    def set_vars_value(self):
        for key in self.var_patterns.keys():
            pattern = re.compile(self.var_patterns[key])
            for string in self.maths:
                cnt = len(re.findall(pattern, string))
                self.vars_value[key] += cnt

    def set_exprs_value(self):
        for key in self.expr_patterns.keys():
            for string in self.maths:
                for pat in self.expr_patterns[key]:
                    pattern = re.compile(pat)
                    cnt = len(re.findall(pattern, string))
                    if cnt:
                        print '===', string
                        print key, cnt
                        print pat
                    self.exprs_value[key] += cnt


def normalize_k_code(char):
    for f in fractions:
        char = char.replace(f, u'\\frac')
    char = re.sub(ur'\\sqrt(?!\s?\[)', '\\sqrt[2]', char)
    char = char.replace(ur'\right.', ur'\right}')
    char = char.replace(ur'\right}', ur'\}')
    char = char.replace(ur'\left{', ur'\{')
    char = char.replace(ur'\left', ur'')
    char = char.replace(ur'\right', ur'')
    char = char.replace(ur'\style{font-family:Times New Roman}{g}', u'g')
    return char


def normalize_parameter(par):  # 参数状态下, 添加 LaTeX 省略的括号{}
    if par == '':
        return par
    else:
        if par[0] in [u'[', u'{'] and par[-1] in [u']', u'}']:
            result = par
        else:
            result = u'{' + par + u'}'
        return result


def normalize_unparameter(par):  # 非参数状态下, 去除多余的{}
    if par == '':
        return par
    else:
        if par[0] in [u'[', u'{'] and par[-1] in [u']', u'}']:
            result = par[1:-1]
        else:
            result = par
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
            elif a.isalpha():
                yield mode, ' ' + a  # 输出非控制序列的字符
            elif a != ' ':
                yield mode, a
        else:
            if a.isalpha():
                char_buffer += a
                if not b.isalpha():
                    char, char_buffer, cmd = ' ' + char_buffer, '\\', UNCOMMAND
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
    # k_code = re.sub(ur'\{\{[^\{\}]*\}\}', lambda x: x.group(0)[1:-1], k_code)  # 去掉重复多余的{}
    k_code = k_code.replace(ur'&', ur' ')  # 去掉公式中的对齐符号, 同时会将'\&'替换成'\ ', 待优化
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
    anni_num = 0
    for i in xrange(idx, length):
        char, level= char_list[i].get('char'), char_list[i].get('level')
        if char_list[i]['used']:
            continue
        if level == ini_level:
            if char in func_parameter_map.keys():
                par_num += func_parameter_map[char]
                expr += char
            elif char in annihilate_map.keys():
                anni_num += annihilate_map[char]
            else:
                if anni_num == 0:
                    if par_num == 0:
                        expr += char
                    else:
                        expr += normalize_parameter(char)
                        par_num += -1
                else:  # 处理吞掉的字符
                    anni_num += -1
            char_list[i]['used'] = USED
        elif level > ini_level:
            if anni_num == 0:
                if par_num == 0:
                    expr += normalize_unparameter(normalize_latex(char_list, level, i, par_buffer))
                else:
                    expr += normalize_parameter(normalize_latex(char_list, level, i, par_buffer))
                    par_num += -1
            else:
                normalize_latex(char_list, level, i, par_buffer)
                anni_num += -1
        else:
            expr += char
            char_list[i]['used'] = USED
            return expr
    return expr