#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-25 19:54

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('10.0.0.168', 27017)
db = client['physics']


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


    item = db.item.find_one({'_id': ObjectId(item_id)})
    k_code = {'desc': item['data']['stem'], 'ans': '', 'exp': ''}
    k_code = _deal_with_qs(item['data']['qs'], k_code)
    return k_code