#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-23 18:14
from itemformulae import ItemFormulae
from itemformulae import normalize_latex
from itemformulae import char_list_generate
from mongodb import get_suit_paper_items
from bson.objectid import ObjectId

def multi_suit_papers(suit_paper_ids):
    item_ids = get_suit_paper_items(suit_paper_ids)
    multi_item_test(item_ids)


def multi_item_test(item_ids):
    for item_id in item_ids:
        formula = ItemFormulae(item_id)
        formula.transfer_k_code()
        formula.set_vars_value()
        formula.set_exprs_value()
        print formula.vars_value
        print formula.exprs_value
        formula.write()


def main():
    print 'hehe'




if __name__ == '__main__':
    main()
