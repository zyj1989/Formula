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
    item_ids = [
        '55dc12c95417d1698debb5bf',
        # '55dae9f65417d10fb3ae80bf',
        # '57b2a672def2976d54a5c780'
    ]
    multi_item_test(item_ids)
    # print normalize_latex(char_list_generate(u'\(s= \\frac12 \)'))
    suit_paper_ids = [
    ObjectId("56b0ae685417d17892497c3f"),
    ObjectId("56b0ae7c5417d17893e9aef8"),
    ObjectId("56b0ae935417d17893e9aef9"),
    ObjectId("56b0aeab5417d178decbb2fa"),
    ObjectId("56b0aec35417d17893e9aefa"),
    ObjectId("56b0aed95417d178decbb2fc"),
    ObjectId("56b0af435417d17892497c42"),
    ObjectId("56b0af625417d178ddc3bb12"),
    ObjectId("56b0afa25417d178decbb2fd"),
    ObjectId("56b0b0305417d178decbb2fe"),
    ObjectId("56b0b0455417d17892497c43"),
    ObjectId("56b0b05b5417d178decbb2ff"),
    # ObjectId("56b0b06f5417d178decbb300"),
    # ObjectId("56b0b0a15417d17893e9af00"),
    # ObjectId("56b0b1945417d178ddc3bb14"),
    # ObjectId("56b0b1a65417d178ddc3bb15"),
    # ObjectId("56b0b1e45417d17892497c44"),
    # ObjectId("56b0b1f75417d178decbb304"),
    # ObjectId("56b0b20c5417d17893e9af02"),
    # ObjectId("56b0b2225417d178ddc3bb17"),
    # ObjectId("56b0b2345417d178decbb306"),
    # ObjectId("56b0b2445417d178ddc3bb18"),
    # ObjectId("56b0b2585417d17892497c46"),
    # ObjectId("56b0b26c5417d178decbb308"),
    # ObjectId("56b0b27e5417d178ddc3bb1a"),
    # ObjectId("56b0b29c5417d17892497c47"),
    # ObjectId("56b0b2cd5417d17893e9af05"),
    # ObjectId("56b0b2ee5417d17893e9af06"),
    # ObjectId("56b0b3095417d178ddc3bb1c"),
    # ObjectId("56b084495417d15fd08624fa"),
    # ObjectId("56b0aba75417d178ddc3bb09"),
    # ObjectId("56b0abc05417d178ddc3bb0a"),
    # ObjectId("56b0ac065417d178decbb2f1"),
    # ObjectId("56b0ac1a5417d17893e9aef5"),
    # ObjectId("56b0ac485417d178decbb2f2"),
    # ObjectId("56b0ac5f5417d178decbb2f3"),
    # ObjectId("56b0ac735417d17893e9aef6"),
    # ObjectId("56b0aca35417d178ddc3bb0c"),
    # ObjectId("56b0acbf5417d17893e9aef7"),
    # ObjectId("56b0ad155417d178ddc3bb0e"),
    # ObjectId("56b0ad2f5417d178decbb2f5"),
    # ObjectId("56b0ad425417d178ddc3bb0f"),
    # ObjectId("56b0ad5f5417d178ddc3bb10"),
    # ObjectId("56b0ad765417d178decbb2f6")
]
# +
# [
#     ObjectId("56d3e1af5417d13da9d3aac0"),
#     ObjectId("56d3e18e5417d13d5366d57b"),
#     ObjectId("56d3e1dd5417d13da9d3aac1"),
#     ObjectId("56d3d8e85417d13d5366d54c"),
#     ObjectId("56d3d8af5417d13d5366d549"),
#     ObjectId("56d3dc505417d13da9d3aa99"),
#     ObjectId("56d3d94d5417d13daa6f9018"),
#     ObjectId("56d3dc8e5417d13da9d3aa9d"),
#     ObjectId("56d3e0c15417d13daa6f9050"),
#     ObjectId("56d3e1245417d13daa6f9059"),
#     ObjectId("56d3cd145417d13d52d805a0"),
#     ObjectId("56d3e2215417d13d52d805ec"),
#     ObjectId("56d3dcb05417d13d52d805b8"),
#     ObjectId("56d3e0fd5417d13d5366d577"),
#     ObjectId("56d3e0675417d13d52d805dd"),
#     ObjectId("56d3e15e5417d13d52d805e8"),
#     ObjectId("56df9e825417d12c861716a7"),
#     ObjectId("56df9bc25417d12c854881a0"),
#     ObjectId("5729a8bddef297653be323b9"),
#     ObjectId("5729c039def297655ef177d3"),
#     ObjectId("5729c65fdef29764f5f7ca03"),
#     ObjectId("572a9e91def297655ef17855"),
#     ObjectId("572ae7e2def297655ef1793f"),
#     ObjectId("572ae944def29764f5f7cb71"),
#     ObjectId("572af653def29764f5f7cbbe"),
#     ObjectId("572af801def297653be32648"),
#     ObjectId("572af9bddef2976518204637"),
#     ObjectId("572bf616def297655ef17a56"),
#     ObjectId("572c3ea7def29764f5f7cdaa"),
#     ObjectId("572c3ed9def2976518204812"),
#     ObjectId("572c439fdef297655ef17b89"),
#     ObjectId("572c52e6def297655ef17beb"),
#     ObjectId("572c54afdef297653be32891"),
#     ObjectId("572c5509def297655ef17c0d"),
#     ObjectId("572ff31edef2973b98eee6c1"),
#     ObjectId("572ff5e0def2973b755fbe96"),
#     ObjectId("573003bddef2973bbb3a31cc"),
#     ObjectId("57302449def2973bdef9819f"),
#     ObjectId("57302631def2973b755fbf1e"),
#     ObjectId("57302f5cdef2973bdef981dd"),
#     ObjectId("57303196def2973bdef981e2"),
#     ObjectId("57303270def2973bbb3a323a"),
#     ObjectId("5730329edef2973b98eee7a4"),
#     ObjectId("5730331ddef2973b755fbf53"),
#     ObjectId("57303a57def2973bbb3a324b"),
#     ObjectId("57303ceddef2973bdef98213"),
#     ObjectId("57303df7def2973b98eee7c4"),
#     ObjectId("57303e9bdef2973b755fbf84"),
#     ObjectId("57304117def2973b98eee7cc"),
#     ObjectId("573041aedef2973b755fbf92"),
#     ObjectId("57304385def2973b755fbf99"),
#     ObjectId("573045d5def2973bdef9823b"),
#     ObjectId("57304c62def2973bbb3a3292"),
#     ObjectId("573051afdef2973bbb3a32aa"),
#     ObjectId("56b081075417d16017af3dc4"),
#     ObjectId("56b081865417d15fd11b55a8"),
#     ObjectId("573157b8def2973bdef98379"),
#     ObjectId("57317ddfdef2973b755fc131")
# ]

    multi_suit_papers(suit_paper_ids)


if __name__ == '__main__':
    main()
