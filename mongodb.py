#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-08-25 19:54

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('10.0.0.168', 27017)
db = client['physics']

def get_item_stem(item_id):
    item = db.item.find_one({'_id': ObjectId(item_id)})
    return item['data']['qs'][0]['exp']