#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from collections import defaultdict

class Formula(object):


    def __init__(self):
        self.var_patterns = {
            'm': ur'\d?{? [mM]}?',
            's': ur'\d?{? [lsxhd]}?',
            't': ur'\d?{? [tT]}?',
            'v': ur'\d?{? [vu]}?',
            'a': ur'\d?{? [ag]}?',
            'F': ur'\d?{? [FNTf]}?',
            'mu': ur'\mu ',
            'omega': ur'\omega ',
            'phi': ur'\phi ',
            'G': ur' G',
            'r': ur' [rR]',
            'E': ur' E'
        }
        # self.mass_pattern = re.compile(self.var_patterns['m'])
        self.vars_value = {}
        for key in self.var_patterns.keys():
            self.vars_value[key] = 0
        self.expr_patterns = {
            'def_v': self.substitute([ur'\\frac{{\delta {s}}}{{\delta {t}}}']),
            'def_a': self.substitute([
                ur'\\frac{{\delta {v}}}{{\delta {t}}}',
                ur'\\frac\{{{v}\}}\{{{t}\}}',
            ]),
            'rel_v_t': self.substitute([ur'{v}={v}\+{a}{t}']),
            'rel_s_t': self.substitute([ur'{s}=(?:{v}{t}\+)?\s*?\\frac\{{1\}}\{{2\}}{a}{t}\^\{{2\}}']),
            'rel_v_s': self.substitute([
                ur'{v}\^\{{2\}}-{v}\^\{{2\}}=2{a}{s}',
                ur'\\frac\{{.*?{v}\^\{{2\}}-{v}\^\{{2\}}\}}\{{2{a}{s}\}}',
                ur'\\frac\{{.*?{v}\^\{{2\}}-{v}\^\{{2\}}\}}\{{2{s}{a}\}}',
                ur'\\frac\{{.*?{v}\^\{{2\}}-{v}\^\{{2\}}\}}\{{2{s}\}}',
                ur'\\frac\{{.*?{v}\^\{{2\}}-{v}\^\{{2\}}\}}\{{2{a}\}}',
            ]),
            'Ek': self.substitute([ur'\\frac\{{1\}}\{{2\}} [mM]{v}\^\{{2\}}']),
            'MC': self.substitute([ur'=?{m}{v}\+{m}{v}=?']),
        }
        self.exprs_value = {}
        for key in self.expr_patterns.keys():
            self.exprs_value[key] = 0


    def substitute(self, expr_list):
        result = []
        for expr in expr_list:
            expr = expr.format(
                m=self.var_patterns['m'],
                s=self.var_patterns['s'],
                t=self.var_patterns['t'],
                v=self.var_patterns['v'],
                a=self.var_patterns['a'],
                F=self.var_patterns['F'],
                mu=self.var_patterns['mu'],
                omega=self.var_patterns['omega'],
                phi=self.var_patterns['phi'],
                G=self.var_patterns['G'],
                r=self.var_patterns['r'],
                E=self.var_patterns['E'],
            )
            result.append(expr)
        return result

