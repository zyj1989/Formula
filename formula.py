#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from collections import defaultdict

class Formula(object):

    def __init__(self):
        self.var_patterns = {
            'm': ur' [mM] ',
            'l': ur' [lsxhd] ',
            't': ur' [tT] ',
            'v': ur' [vu] ',
            'a': ur' [ag] ',
            'F': ur' [FNTf] ',
            'mu': ur'\mu',
            'omega': ur'\omega',
            'phi': ur'\phi',
            'G': ur' G ',
            'r': ur' [rR] ',
            'E': ur' E '
        }

        # self.mass_pattern = re.compile(self.var_patterns['m'])
        self.vars_value = {}
        for key in self.var_patterns.keys():
            self.vars_value[key] = 0
