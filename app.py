
from flask import Flask
from flask_smorest import Api
from resources.store import blp as StoreBlueprint
from resources.items import blp as ItemBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Warehouse REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)


''' 
Obsolete Code 

# stores = [
#     {
#         "name": "My Store",
#         "items": {
#             "name": "Chair",
#             "price": 15.99
#         }
#     }
# ]


# get all stores
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


# get all items
@app.get("/items")
def get_items():
    return {"items": list(items.values())}


# create new store
@app.post("/store")
def create_store():
    data = request.get_json()

    if "name" not in data:
        abort(400, message="Bad Request, 'name' must be included")

    for store in stores.values():
        if data["name"] == store["name"]:
            abort(400, message="This store name is already used.")
    storeId = uuid.uuid4().hex
    # newStore = {"name": data["name"], "items": []}
    # kwargs bcoz data is a str else data.copy() or just data
    store = {**data, "store_id": storeId}
    stores[storeId] = store
    return store, 201


# dynamic
# create new item
@app.post("/item")
def create_item():
    data = request.get_json()

    if "price" not in data or "store_id" not in data or "name" not in data:
        abort(400, message="Bad Request, ensure 'price', 'name' and 'store_id' are present")

    if data["store_id"] not in stores:
        # return {"error": "Store not found"}, 404
        abort(404, message="Store not found.")

    for item in items.values():
        if data["name"] == item["name"] and data["store_id"] == item["store_id"]:
            abort(400, message="Item already exists")

    itemId = uuid.uuid4().hex
    item = {**data, "item_id": itemId}
    items[itemId] = item
    return item, 201


# get item
@app.get("/item/<string:itemId>")
def get_item(itemId):
    try:
        return items[itemId]
    except KeyError:
        # return {"error": "item not found"}, 404
        abort(404, message="Item not found.")


# get store
@app.get("/store/<string:storeId>")
def get_store_data(storeId):
    try:
        return stores[storeId]
    except KeyError:
        # return {"error": "Store not found"}, 404
        abort(400, message="Bad Request, 'name' must be included")


# delete item
@app.delete("/item/<string:itemId>")
def delete_item(itemId):
    try:
        del items[itemId]
        return {"message": "item deleted"}
    except KeyError:
        abort(404, message="Item not found")


# update item
@app.put("/item/<string:itemId>")
def update_item(itemId):
    data = request.get_json()

    if "name" not in data or "price" not in data:
        abort(400, message="Bad Request, 'name' or 'price' must be included")

    try:
        item = items[itemId]
        item.update(data)  # item |= data  # Py.3.9 updates a dict IKR!!

        return item
    except KeyError:
        abort(404, message="Item not found")


# get all items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# delete store
@app.delete("/store/<string:storeId>")
def delete_store(storeId):
    try:
        del stores[storeId]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")
'''
