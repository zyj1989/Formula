#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14
from itemformulae import ItemFormulae


def main():
    formula = ItemFormulae('55e3e6e35417d113d1c0c9f4')
    formula.transfer_k_code()
    print formula.math
    formula.set_vars_value()
    print formula.vars_value

if __name__ == '__main__':
    main()
