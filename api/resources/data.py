from flask import jsonify
from flask_restful import Resource, reqparse

from mongo import mongo


class Data(Resource):

    def get(self):

        data_pipeline = [
            {
                "$sort":
                    {
                        "_id": -1
                    }
            },
            {
                "$limit": 100
            },
            {
                "$project":
                    {
                        "_id": 0
                    }
            }
        ]

        data_info = list(mongo.db['tribes-data'].aggregate(pipeline=data_pipeline))
        if data_info:
            return jsonify({"status": "ok", "data": data_info})
        else:
            return {"response": "no data found"}