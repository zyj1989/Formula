#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re


class Formula(object):


    def __init__(self):
        self.var_patterns = {
            'm': ur'\d?(?:[\[\(\{])? [mM]}?',
            's': ur'\d?{? [lsxyzhdLrR]}?',
            't': ur'\d?{? [tT]}?',
            'v': ur'[\[\(\{]?\d? [vu][\]\)\}]?',
            'a': ur'\d?{? [ag]}?',
            'F': ur'\d?{? (?:[FNTf]|m g)}?',  # 重力等效于力
            'mu': ur' \\mu',
            'omega': ur' \\omega',
            'phi': ur' \\phi',
            'G': ur' G',
            'r': ur' [rR]',
            'E': ur' E',
            'sqr': ur'\^\{2\}',
            'cubic': ur'\^\{3\}',
            'k': ur' k',
            'pi': ur' \\pi',
            'W': ur' W',
            'P': ur' P',
            'KE': ur' \\frac\{{1\}}\{{2\}}\d?(?:[\[\(\{])? [mM]}?[\[\(\{]?\d? [vu][\]\)\}]?\^\{2\}',

        }
        self.vars_value = {}
        for key in self.var_patterns.keys():
            self.vars_value[key] = 0
        self.expr_patterns = {
            'def_v': self.substitute([ur'\\frac{{\Delta {s}}}{{\Delta {t}}}']),
            'def_a': self.substitute([
                ur'\\frac{{\Delta {v}}}{{\Delta {t}}}',
                ur'\\frac\{{{v}\}}\{{{t}\}}',
            ]),
            'rel_v_t': self.substitute([ur'{v}={v}[-\+]{a}{t}']),
            'rel_s_t': self.substitute([
                ur'{s}=({v}{t}\+)?\s*?\\frac\{{1\}}\{{2\}}{a}{t}{sqr}',
            ]),
            'rel_v_s': self.substitute([
                ur'{v}{sqr}-{v}{sqr}=2{a}{s}',
                ur'{v}{sqr}=2{a}{s}\+{v}{sqr}',
                ur'{v}{sqr}={v}{sqr}\+2{a}{s}',
                ur' \\frac\{{.*?{v}{sqr}-{v}{sqr}\}}\{{2{a}{s}\}}',
                ur' \\frac\{{.*?{v}{sqr}-{v}{sqr}\}}\{{2{s}{a}\}}',
                ur' \\frac\{{.*?{v}{sqr}-{v}{sqr}\}}\{{2{s}\}}',
                ur' \\frac\{{.*?{v}{sqr}-{v}{sqr}\}}\{{2{a}\}}',
            ]),
            'CM': self.substitute([ur'=?{m}{v}\+{m}{v}=?']),
            'v_half_s': self.substitute([
                ur'{v}= \\sqrt\[2\]\{{ \\frac\{{{v}{sqr}\+{v}{sqr}\}}',
            ]),
            'v_half_t': self.substitute([
                ur'{s}= \\frac\{{{v}\+{v}\}}\{{2\}}{t}',
                ur'{v}= \\frac\{{{v}\+{v}\}}\{{2\}}',
            ]),
            'st_sequence': self.substitute([
                ur'1: \\sqrt\[2\]\{{2\}}: \\sqrt\[2\]\{{3\}}',
                ur'1:3:5',
            ]),
            'delta_s_each_t': self.substitute([
                ur'{a}= \\frac\{{{s}-{s}\}}\{{{t}{sqr}\}}',
                ur'{a}= \\frac\{{ \\Delta{s}\}}\{{{t}{sqr}\}}',
            ]),
            'free_fall': self.substitute([
                ur' \\sqrt\[2\]\{{ \\frac\{{2{s}\}}\{{{a}\}}\}}',
            ]),
            'Hooke_Law': self.substitute([
                ur'{F}= k{s}',
                ur' \\frac\{{.*?{F}\}}\{{ k\}}',
            ]),
            'resistance': self.substitute([
                ur'{mu}{F}',
            ]),
            'f_resolve': self.substitute([
                ur'{F} \\sin',
                ur'{F} \\cos',
            ]),
            'N2L': self.substitute([
                ur'{F}={m}{a}',
            ]),
            'v_resolve': self.substitute([
                ur'{v} \\sin',
                ur'{v} \\cos',
            ]),
            'projectile': self.substitute([
                ur' \\frac\{{{a}{t}\}}\{{{v}\}}',
            ]),
            'rel_v_omega': self.substitute([
                ur' \\omega{r}',
            ]),
            'a_n': self.substitute([
                ur' \\frac\{{{v}{sqr}\}}\{{{r}\}}',
                ur' \\omega{sqr}{r}',
            ]),
            'Kepler': self.substitute([
                ur' \\frac\{{{a}{cubic}\}}\{{{t}{sqr}\}}',
            ]),
            'rel_v_T': self.substitute([
                ur' \\frac\{{2 \\pi\}}\{{{t}\}}',
                ur' \\frac\{{2 \\pi{r}\}}\{{{t}\}}',
            ]),
            'Gravity': self.substitute([
                ur'{G} \\frac\{{{m}{m}\}}\{{{r}{sqr}\}}',
                ur' \\frac\{{{G}{m}{m}\}}\{{{r}{sqr}\}}',
            ]),
            'g_accom': self.substitute([
                ur' \\frac\{{4{pi}{sqr}{r}{cubic}\}}\{{{G}{t}{sqr}\}}',
            ]),
            'work': self.substitute([
                ur' W=(-)?{F}{s}( \\cos)?',
            ]),
            'power': self.substitute([
                ur'{P}=(-)?{F}{v}( \\cos)?',
                ur'{P}= \\frac\{{{W}\}}\{{{t}\}}',
                ur' \\frac\{{{P}\}}\{{{F}\}}',
            ]),
            'GPE': self.substitute([
                ur'{m}{a}{s}',
            ]),
            'LKE': self.substitute([
                ur' \\frac\{{1\}}\{{2\}}{m}{v}{sqr}- \\frac\{{1\}}\{{2\}}{m}{v}{sqr}',
            ]),
            'CME': self.substitute([
                ur'=?{m}{v}\+{m}{v}=?'
            ]),

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
                sqr=self.var_patterns['sqr'],
                cubic=self.var_patterns['cubic'],
                k=self.var_patterns['k'],
                pi=self.var_patterns['pi'],
                W=self.var_patterns['W'],
                P=self.var_patterns['P'],
                KE=self.var_patterns['KE'],
            )
            result.append(expr)
        return result

