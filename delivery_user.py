from flask import Blueprint, request, jsonify, session
from flask_pymongo import PyMongo
import bcrypt
import json
from bson.objectid import ObjectId
from database import mongo

delivery_user = Blueprint('delivery_user', __name__)

@delivery_user.route('/api/shop/',methods=['POST'])
def getAllShop():
    try:
        shops = mongo.db.shop
        users = mongo.db.user
        current_user = users.find_one({'_id':ObjectId(request.json['uid'])})
        zone = current_user['zone']
        output=[]
        shops_in_zone=shops.find({'zone':int(zone)})
        if shops_in_zone is None:
            return jasonify({'result':'No shops exist in this zone','status':201})
        else:
            for shop in shops_in_zone:
                output.append({'id':str(shop['_id']),'name':shop['shopname'],'address':shop['address'],'phone':shop['phone'],'type':shop['type'],'items':shop['items']})
            return jsonify({'result':output,'status':201})


    except Exception as e:
        raise e
        return jsonify({'result':"failed",'status':500})


@delivery_user.route('/api/items/',methods=['GET'])
def getAllItems():
    try:
        items = mongo.db.item
        output=[]
        itemsCursor=items.find()
        if itemsCursor is None:
            return jsonify({'result':'No shops exist in this zone','status':201})
        else:
            for sitem in itemsCursor:
                output.append({'itemId':str(sitem['_id']),'itemname':sitem['itemname'],'price':sitem['price'],'type':str(sitem['type']),'unitqty':sitem['unitqty']})
            return jsonify({'result':output,'status':201})


    except Exception as e:
        raise e
        return jsonify({'result':"failed",'status':500})

@delivery_user.route('/api/orders/<uid>',methods=['GET'])
def getAllOrders(uid):
    try:
        orders = mongo.db.order
        output=[]
        userOrders=orders.find({'uid':uid})
        if userOrders is None:
            return jsonify({'result':'Yoy have not ordered anything','status':201})
        else:
            for sorder in userOrders:
                output.append({'orderId':str(sorder['_id']),'items':sorder['itemnames'],'qty':sorder['qty'],'amount':sorder['amount'],'time':sorder['time'],'status':sorder['status']})
            return jsonify({'result':output,'status':201})
    except Exception as e:
        raise e
        return jsonify({'result':"failed",'status':500})


@delivery_user.route('/api/singleorder/<oid>',methods=['GET'])
def getSingleOrders(oid):
    try:
        orders = mongo.db.order
        items = mongo.db.item
        output=[]
        sorder=orders.find_one({'_id':ObjectId(oid)})
        current_items = sorder['items']
        current_prices = []
        for it in current_items:
            itemf = items.find_one({'_id':ObjectId(it)})
            current_prices.append(itemf['price'])
        return jsonify({'orderId':str(sorder['_id']),'items':sorder['itemnames'],'qty':sorder['qty'],'amount':sorder['amount'],'time':sorder['time'],'status':sorder['status'],'itemprices':current_prices})
    except Exception as e:
        raise e
        return jsonify({'result':"failed",'status':500})

@delivery_user.route('/api/orders',methods=['POST'])
def pushOrder():
    try:
        orders = mongo.db.order
        id = orders.insert({
        'items':request.json['items'],
        'itemnames':request.json['itemnames'],
        'qty':request.json['qty'],
        'uid':request.json['uid'],
        'amount':request.json['amount'],
        'time':request.json['time'],
        'status':request.json['status'],
        })

        return jsonify({'result':str(id),'status':201})
    except Exception as e:
        raise e
        return jsonify({'result':"failed",'status':500})
