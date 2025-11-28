import uuid
from flask_smorest import Blueprint, abort  # noqa
from flask import request
from flask.views import MethodView
from db import items, stores

# Blueprint is a way to organize a group of related routes and views
bp = Blueprint('items', __name__, description='Operations on items')

# With /item crud operations
@bp.route('/item')
class ItemList(MethodView):
    """List all items."""
    def get(self):
        return {'items': list(items.values())}
      
    def post(self):
        request_data = request.get_json()
        if (
            'price' not in request_data
            or 'name' not in request_data
            or 'store_id' not in request_data
        ):
            abort(400, message='Missing required fields')

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
    """Operations for a single item."""
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

    def put(self, item_id):
        request_data = request.get_json()
        if (
            'price' not in request_data
            or 'name' not in request_data
        ):
            abort(400, message='Missing required fields')

        try:
            item = items[item_id]
            item.update(request_data)
            return item, 200
        except KeyError:
            abort(404, message='Item not found')
