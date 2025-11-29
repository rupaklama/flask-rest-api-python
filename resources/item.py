import uuid
from flask_smorest import Blueprint, abort  # noqa
from flask import request
from flask.views import MethodView
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

# Blueprint is a way to organize a group of related routes and views
bp = Blueprint('items', __name__, description='Operations on items')

# With /item crud operations
@bp.route('/item')
class ItemList(MethodView):
    # many=True indicates that we expect a list of items to be returned
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
      
    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    # request_data is the validated data from the request body
    def post(self, request_data):
        # if (
        #     'price' not in request_data
        #     or 'name' not in request_data
        #     or 'store_id' not in request_data
        # ):
        #     abort(400, message='Missing required fields')

        for item in items.values():
            if item['name'] == request_data['name']:
                abort(400, message='Item with the same name already exists')

        try:
            stores[request_data['store_id']]
        except KeyError:
            abort(404, message='Store not found')

        item_id = uuid.uuid4().hex
        # double asterisk (**) takes all key-value pairs from the request_data dictionary 
        # and "unpacks" them directly into the new dictionary
        new_item = {
            **request_data,
            'id': item_id,
        }
        items[new_item['id']] = new_item
        return new_item, 201

# With /item/<item_id> crud operations
@bp.route('/item/<string:item_id>')
class ItemDetail(MethodView):
    # Decorator generating an endpoint response 
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='Item not found')

    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': 'Item deleted'}, 200
        except KeyError:
            abort(404, message='Item not found')
            
    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    # request_data comes before item_id because of the order of parameters in the method
    def put(self, request_data, item_id):
        try:
            item = items[item_id]
            item.update(request_data)
            return item, 200
        except KeyError:
            abort(404, message='Item not found')
