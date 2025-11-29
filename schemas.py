# marshmallow is a library for object serialization/deserialization and validation
from marshmallow import Schema, fields


class StoreCreateSchema(Schema):
    id = fields.Str(dump_only=True)  
    name = fields.Str(required=True)


class ItemSchema(Schema):
    # dump_only=True means this field is only for serialization (output) in the API responses
    id = fields.Str(dump_only=True) 
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    
