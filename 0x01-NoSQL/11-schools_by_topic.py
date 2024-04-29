#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def schools_by_topic(mongo_collection, topic):
    """ returns list of school that have a specific topic """
    documents = mongo_collection.find({"topics": topic})
    return list(documents)
