#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re


class Formula(object):


    def __init__(self):
        self.var_patterns = {
            'm': ur'[\[\(]?\d* [mM][\]\)]?',
            's': ur'[\[\(]?\d* [lsxyzhdLrR][\)\]]?',
            't': ur'[\[\(]?\d* [tT][\]\)]?',
            'v': ur'[\[\(]?\d* [vu][\]\)]?',
            'a': ur'[\[\(]?\d* [ag][\]\)]?',
            'r': ur'[\[\(]?\d* [rR][\]\)]?',
            'F': ur'[\[\(]?\d* (?:[FNTf]|m g)[\]\)]?',  # 重力等效于力
            'mu': ur' \\mu',
            'omega': ur' \\omega',
            'phi': ur' \\phi',
            'G': ur'[\[\(]?\d* G[\]\)]?',
            'E': ur'[\[\(]?\d* E[\]\)]?',
            'sqr': ur'\^\{2\}',
            'cubic': ur'\^\{3\}',
            'half': ur' \\frac\{1\}\{2\}',
            'k': ur' k',
            'pi': ur'[\[\(]?\d* \\pi[\]\)]?',
            'W': ur' [\[\(]?\d* W[\]\)]?',
            'P': ur' [\[\(]?\d* P[\]\)]?',
            'C': ur' [\[\(]?\d* C[\]\)]?',
            'I': ur' [\[\(]?\d* [Ii][\]\)]?',
            'KE': ur' \\frac\{1\}\{2\}[\[\(]?\d* [mM][\]\)]?[\[\(]?\d* [vu][\]\)]?\^\{2\}',
            'q': ur'[\[\(]?\d* [Qqe][\]\)]?',
            'U': ur'[\[\(]?\d* [UE][\]\)]?',
            'e': ur' \\varepsilon',
            'A': ur'[\[\(]?\d* [SsA][\]\)]?',
            'B': ur'[\[\(]?\d* B[\]\)]?',
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
            'Hookes_Law': self.substitute([
                ur'{F}= k{s}',
                ur' \\frac\{{.*?{F}\}}\{{ k\}}',
            ]),
            'resistance': self.substitute([
                ur'{mu}{F}',
            ]),
            'f_resolve': self.substitute([
                ur'{F} (\\sin|\\cos)',
            ]),
            'N2L': self.substitute([
                ur'{F}={m}{a}',
            ]),
            'v_resolve': self.substitute([
                ur'{v} (\\sin|\\cos)',
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
                ur'{half}{m}{v}{sqr}-{half}{m}{v}{sqr}',
            ]),
            'CME': self.substitute([
                ur'{half}{m}{v}{sqr}\+{half}{m}{v}{sqr}',
                ur'{m}{a}{s}= \\frac\{{1\}}\{{2\}}{m}{v}{sqr}([-\+] \\frac\{{1\}}\{{2\}}{m}{v}{sqr})?',
            ]),
            'Coulombs_Law': self.substitute([
                ur'{k} \\frac\{{{q}{q}\}}\{{{s}{sqr}\}}',
                ur'{k} \\frac\{{{q}{sqr}\}}\{{{s}{sqr}\}}',
            ]),
            'specific_charge': self.substitute([
                ur' \\frac\{{{q}\}}\{{{m}\}}',
            ]),
            'def_E': self.substitute([
                ur' \\frac\{{{F}\}}\{{{q}\}}',
            ]),
            'E_charge': self.substitute([
                ur'{k} \\frac\{{{q}\}}\{{{s}{sqr}\}}',
            ]),
            'def_EPE': self.substitute([
                ur' \\frac\{{{E}\}}\{{{q}\}}',
            ]),
            'rel_U_E': self.substitute([
                ur'{E}= \\frac\{{{U}\}}\{{{s}\}}',
                ur'{U}={E}{s}',
            ]),
            'def_capacity': self.substitute([
                ur' \\frac\{{{q}\}}\{{{U}\}}',
                ur'{q}={U}{C}',
                ur' \\frac\{{{q}\}}\{{{C}\}}',
            ]),
            'capacity': self.substitute([
                ur' \\frac\{{({e})?{A}\}}\{{4{pi}{k}{s}\}}',
                ur' \\frac\{{({e})?{A}\}}\{{4{k}{pi}{s}\}}',  # 由于旧版题库傻逼 所以兼容一下把k写到pi前面的错误公式风格
            ]),
            'accerlerate_charge': self.substitute([
                ur'{U}{q}={half}{m}{v}{sqr}',
                ur'{q}{U}={half}{m}{v}{sqr}',
                ur'{E}{q}{s}={half}{m}{v}{sqr}',
                ur'{q}{E}{s}={half}{m}{v}{sqr}',
            ]),
            'def_I': self.substitute([
                ur'{I}= \\frac\{{{q}\}}\{{{t}\}}',
                ur'{q}={I}{t}',
            ]),
            'Ohms_Law': self.substitute([
                ur'{U}={I}{r}',
                ur'{U}={r}{I}',
                ur'{I}= \\frac\{{{U}\}}\{{{r}\}}',
                ur'{r}= \\frac\{{{U}\}}\{{{I}\}}',
            ]),
            'Joule_power': self.substitute([
                ur'{P}={U}{I}',
            ]),
            'Joules_Law': self.substitute([
                ur'{I}{sqr}{r}',
            ]),
            'resistance_law': self.substitute([
                ur'{r}= \\rho \\frac\{{{s}\}}\{{{A}\}}',
            ]),
            'def_B': self.substitute([
                ur'{B}= \\frac\{{{F}\}}\{{{I}{s}\}}',
                ur'{B}= \\frac\{{{F}\}}\{{{s}{I}\}}',
                ur'{F}={B}{I}{s}',
                ur'{F}={I}{B}{s}',
                ur'{F}={I}{s}{B}',
            ]),
            'def_Phi': self.substitute([
                ur' \\varPhi={B}{A}',
            ]),
            'Lorentz_F': self.substitute([
                ur'{q}{v}{B}',
                ur'{q}{B}{v}',
                ur'{B}{q}{v}',
            ]),
            'mag_circle_motion': self.substitute([
                ur' \\frac\{{{m}{v}\}}\{{{B}{q}\}}',
                ur' \\frac\{{{m}{v}\}}\{{{q}{B}\}}',
                ur' \\frac\{{{m}{v}\}}\{{{B}{r}\}}',
                ur' \\frac\{{{m}{v}\}}\{{{r}{B}\}}',
                ur' \\frac\{{{pi}{m}\}}\{{{B}{q}\}}',
                ur' \\frac\{{{pi}{m}\}}\{{{q}{B}\}}',
            ])

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
                half=self.var_patterns['half'],
                k=self.var_patterns['k'],
                pi=self.var_patterns['pi'],
                W=self.var_patterns['W'],
                P=self.var_patterns['P'],
                C=self.var_patterns['C'],
                KE=self.var_patterns['KE'],
                q=self.var_patterns['q'],
                e=self.var_patterns['e'],
                U=self.var_patterns['U'],
                A=self.var_patterns['A'],
                B=self.var_patterns['B'],
                I=self.var_patterns['I'],
            )
            result.append(expr)
        return result

