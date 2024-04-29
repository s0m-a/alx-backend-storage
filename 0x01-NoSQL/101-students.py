#!/usr/bin/env python3
""" MongoDB operation with Python """


def top_students(mongo_collection):
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]
    return top_student
