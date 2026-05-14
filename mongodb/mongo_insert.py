from pymongo import MongoClient

# connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# create database
db = client["northstar_db"]

print("Connected successfully")

import pandas as pd

data = pd.read_csv("cleaned_main.csv")
complaints = pd.read_csv("complaints.csv")
incidents = pd.read_csv("incidents.csv")
app_events = pd.read_csv("app_events.csv")

print("Data loaded")

# group complaints
complaints_grouped = complaints.groupby('order_id').apply(
    lambda x: x.to_dict('records')
).to_dict()

# group incidents
incidents_grouped = incidents.groupby('delivery_id').apply(
    lambda x: x.to_dict('records')
).to_dict()

# group events
events_grouped = app_events.groupby('order_id').apply(
    lambda x: x.to_dict('records')
).to_dict()

print("Grouping done")

import math

def clean_nan(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

documents = []

for _, row in data.iterrows():
    doc = {
        "order_id": row['order_id'],
        "customer_id": row.get('customer_id'),

        "zones": {
            "pickup": row.get('pickup_zone'),
            "dropoff": row.get('dropoff_zone')
        },

        "delivery": {
            "driver_id": row.get('driver_id'),
            "vehicle_id": row.get('vehicle_id'),
            "delivery_time_hours": row.get('delivery_time_hours'),
            "delay_flag": bool(row.get('delay_flag')),
            "manual_route_override_count": row.get('manual_route_override_count'),
            "fuel_cost": row.get('fuel_or_charge_cost')
        },

        "complaints": complaints_grouped.get(row['order_id'], []),
        "incidents": incidents_grouped.get(row['delivery_id'], []),
        "events": events_grouped.get(row['order_id'], [])
    }

    # clean NaN values
    doc = {k: clean_nan(v) for k, v in doc.items()}

    documents.append(doc)

print("Documents created:", len(documents))

collection = db["order_journeys"]

# clear existing data
collection.delete_many({})

# insert new data
collection.insert_many(documents)

print("Data inserted successfully")

# ----------------------------
# CREATE INDEXES (IMPORTANT)
# ----------------------------

print("Creating indexes...")

# Indexes for order_journeys
collection.create_index("order_id", unique=True)
collection.create_index("customer_id")
collection.create_index("delivery.delay_flag")
collection.create_index("delivery.driver_id")
collection.create_index("zones.dropoff")
collection.create_index("delivery.manual_route_override_count")

print("Indexes for order_journeys created")