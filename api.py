from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

data_store = {}

class  DataResource(Resource):
    def get(self, item_id):
        item = data_store.get(item_id)
        if not item:
            return {"error": "Item not found"}, 404
        return item, 200

    def post(self, item_id):
        data = request.get_json()
        data_store[item_id] = data
        return {"message": "Item added", "item": data}, 201

    def delete(self, item_id):
        if item_id in data_store:
            del data_store[item_id]
            return {"message": "Item deleted"}, 200
        return {"error": "Item not found"}, 404

api.add_resource(DataResource, '/api/item/<string:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
