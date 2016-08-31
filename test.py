#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14
from itemformulae import ItemFormulae
from itemformulae import normalize_latex
from itemformulae import char_list_generate


def main():
    formula = ItemFormulae('57845a70def29763faade783')
    formula.transfer_k_code()
    print formula.math
    formula.set_exprs_value()
    formula.set_vars_value()
    print formula.vars_value
    print formula.exprs_value
    # print normalize_latex(char_list_generate(u'\(s= \\frac12 \)'))
if __name__ == '__main__':
    main()
