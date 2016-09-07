#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-25 19:54

from pymongo import MongoClient
from bson.objectid import ObjectId



db_r = MongoClient('10.0.0.168', 27017)['physics']
db_w = MongoClient('10.0.0.76', 27017)['zyj']


def write_in_db(_id, math, vars_value, exprs_value, relation):
    db_w.itemformulae.update({
        '_id': ObjectId(_id)
    },{
        '_id': ObjectId(_id),
        'math': math,
        'vars': vars_value,
        'exprs': exprs_value,
        'relation': relation,
    }, True)



def get_suit_paper_items(suit_paper_ids):
    item_id_list = []
    for suit_paper_id in suit_paper_ids:
        suit_paper = db_r.suit_papers.find_one({
            '_id': ObjectId(suit_paper_id)
        },{
            'parts': 1
        })
        for item in suit_paper['parts'][0]:
            item_id_list.append(item['item_id'])
    return item_id_list


def get_item_k_code(item_id):

    def _deal_with_qs(qs, k_code):
        for q in qs:
            if 'qs' in q:
                k_code = _deal_with_qs(q['qs'], k_code)
            k_code['desc'] += q['desc']
            if 'ans' in q:
                for ans in q['ans']:
                    k_code['ans'] += u'{}'.format(ans)
            if 'exp' in q:
                k_code['exp'] += q['exp']
        return k_code

    item = db_r.item.find_one({'_id': ObjectId(item_id)})
    k_code = {'desc': item['data']['stem'], 'ans': '', 'exp': ''}
    k_code = _deal_with_qs(item['data']['qs'], k_code)
    return k_code