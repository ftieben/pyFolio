# -*- coding: utf-8 -*-

from datetime import datetime
from influxdb import InfluxDBClient


def write_to_influx(df):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    """Instantiate the connection to the InfluxDB client."""
    host = "localhost"
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'demo'

    client = InfluxDBClient(host, port, user, password, dbname)

    # print("Create database: " + dbname)
    client.create_database(dbname)

    # print("Write Data")
    for index, row in df.iterrows():
        payload = [
            {
                "measurement": row["name"],
                "time": current_time,
                "fields": {
                    "amount": row["amount"],
                    "price": row["price"],
                    "sum": row["sum"],
                }
            }
        ]
        # print(payload)
        client.write_points(payload)
    return True


def write_row_to_influx(row):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    """Instantiate the connection to the InfluxDB client."""
    host = "localhost"
    port = 8086
    user = 'root'
    password = 'root'
    dbname = 'demo'

    client = InfluxDBClient(host, port, user, password, dbname)

    client.create_database(dbname)

    payload = [
        {
            "measurement": row["name"],
            "time": current_time,
            "fields": {
                "amount": float(row["amount"]),
                "price": float(row["price"]),
                "sum": float(row["sum"]),
            }
        }
    ]

    client.write_points(payload)

    return True
