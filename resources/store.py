import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store")
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        # data = request.get_json()

        # if "name" not in data:
        #     abort(400, message="Bad Request, 'name' must be included")

        for store in stores.values():
            if data["name"] == store["name"]:
                abort(400, message="This store name is already used.")
        storeId = uuid.uuid4().hex
        # newStore = {"name": data["name"], "items": []}
        # kwargs bcoz data is a str else data.copy() or just data
        store = {**data, "store_id": storeId}
        stores[storeId] = store
        # return store, 201
        return store


@blp.route("/store/<string:storeId>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, storeId):
        try:
            return stores[storeId]
        except KeyError:
            # return {"error": "Store not found"}, 404
            abort(400, message="Bad Request, 'name' must be included")

    def delete(self, storeId):
        try:
            del stores[storeId]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")
