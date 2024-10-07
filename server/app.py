#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        res_dict_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(res_dict_list), 200)

    def post(self):
        try:
            # Ensure the required data fields are present
            data = request.json
            name = data.get("name")
            image = data.get("image")
            price = data.get("price")

            if not name or not price:
                return make_response(
                    jsonify({"error": "Missing 'name' or 'price' field"}), 400
                )

            new_record = Plant(
                name=name,
                image=image,
                price=price
            )

            db.session.add(new_record)
            db.session.commit()

            response_dict = new_record.to_dict()
            return make_response(jsonify(response_dict), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(Plants, "/plants")

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if plant:
            response_dict = plant.to_dict()
            return make_response(jsonify(response_dict), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
