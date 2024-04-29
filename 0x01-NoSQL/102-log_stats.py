#!/usr/bin/env python3
""" MongoDB Operations with Python """
from pymongo import MongoClient


def get_logs_stats():
    """Get statistics about Nginx logs stored in MongoDB."""
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_count = {method: collection.count_documents({"method": method}) for method in methods}

    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    top_ips_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(collection.aggregate(top_ips_pipeline))

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")
    print("IPs:")
    for ip_info in top_ips:
        print(f"\t{ip_info['_id']}: {ip_info['count']}")

if __name__ == "__main__":
    get_logs_stats()
