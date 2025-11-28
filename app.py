import uuid
from flask import Flask, request 
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Store API!"

@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}
  
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message='Store not found')

@app.post('/store')
def create_store():
    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, message='Missing required field: name')
        
    for store in stores.values():
        if store['name'] == request_data['name']:
            abort(400, message='Store with the same name already exists')
    
    store_id = uuid.uuid4().hex
    new_store = {
      # double asterisk (**) takes all key-value pairs from the request_data dictionary 
      # and "unpacks" them directly into the new dictionary
        **request_data,
        'id': store_id,
    }
    stores[new_store['id']] = new_store
    return new_store, 201

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': 'Store deleted'}, 200
    except KeyError:
        abort(404, message='Store not found')


@app.get('/item')
def get_items():
    return 'hello, items!'
    return {'items': list(items.values())}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message='Item not found')

@app.post('/item')
def create_item():
    request_data = request.get_json()
    if (
      'price' not in request_data or
      'name' not in request_data or
      'store_id' not in request_data
    ):
        abort(400, message='Missing required fields')
        
    for item in items.values():
        if item['name'] == request_data['name'] and item['store_id'] == request_data['store_id']:
            abort(400, message='Item with the same name already exists in this store')

    if request_data['store_id'] not in stores:
        abort(404, message='Store not found')
        
    item_id = uuid.uuid4().hex
    new_item = {
        **request_data,
        'id': item_id,
    }
    items[new_item['id']] = new_item
    return new_item, 201
  

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
      del items[item_id]
      return {'message': 'Item deleted'}, 200
    except KeyError:
      abort(404, message='Item not found')
      
@app.put('/item/<string:item_id>')
def update_item(item_id):
    request_data = request.get_json()
    if (
      'price' not in request_data or
      'name' not in request_data 
    ):
        abort(400, message='Missing required fields')
        
    try:
        item = items[item_id]
        item.update(request_data)
        return item, 200
    except KeyError:
        abort(404, message='Item not found')
