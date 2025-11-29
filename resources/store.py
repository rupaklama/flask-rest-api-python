import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreCreateSchema

# Blueprint is a way to organize a group of related routes and views
bp = Blueprint('stores', __name__, description='Operations on stores')

# MethodView allows us to define class-based views(api methods) for our similar endpoints
# With /store crud operations
@bp.route('/store')
class StoreList(MethodView):
    @bp.response(200, StoreCreateSchema(many=True))
    def get(self):
        return stores.values()

    @bp.arguments(StoreCreateSchema)
    @bp.response(201, StoreCreateSchema)
    def post(self, request_data):
        for store in stores.values():
            if store['name'] == request_data['name']:
                abort(400, message='Store with the same name already exists')

        store_id = uuid.uuid4().hex
        # double asterisk (**) takes all key-value pairs from the request_data dictionary 
        # and "unpacks" them directly into the new dictionary
        new_store = {
            **request_data,
            'id': store_id,
        }
        stores[new_store['id']] = new_store
        return new_store, 201

# With /store/<store_id> crud operations
@bp.route('/store/<string:store_id>')
class StoreDetail(MethodView):
    @bp.response(200, StoreCreateSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found')

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {'message': 'Store deleted'}, 200
        except KeyError:
            abort(404, message='Store not found')
