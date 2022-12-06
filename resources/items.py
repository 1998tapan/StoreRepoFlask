import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items")


@blp.route("/item")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())}
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        # params - data - it's the json sent by request, captured and validated by schema

        # data = request.get_json()
        # not required bcoz it is fetched by schema instead and validated

        # this validation is no longer required, performed by schema
        # if "price" not in data or "store_id" not in data or "name" not in data:
        #     abort(
        #         400, message="Bad Request, ensure 'price', 'name' and 'store_id' are present")

        if data["store_id"] not in stores:
            abort(404, message="Store not found.")

        for item in items.values():
            if data["name"] == item["name"] and data["store_id"] == item["store_id"]:
                abort(400, message="Item already exists")

        itemId = uuid.uuid4().hex
        item = {**data, "item_id": itemId}
        items[itemId] = item
        # return item, 201
        return item


@blp.route("/item/<string:itemId>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, itemId):
        try:
            return items[itemId]
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, itemId):
        # data = request.get_json()

        # if "name" not in data or "price" not in data:
        #     abort(400, message="Bad Request, 'name' or 'price' must be included")

        try:
            item = items[itemId]
            item.update(data)  # item |= data  # Py.3.9 updates a dict IKR!!

            return item
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, itemId):
        try:
            del items[itemId]
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message="Item not found")
