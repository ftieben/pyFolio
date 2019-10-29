# -*- coding: utf-8 -*-

from datetime import datetime
from influxdb import DataFrameClient


def write_to_influx(df):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    for index, row in df.iterrows():
        df.loc[index, 'time'] = current_time

    """Instantiate the connection to the InfluxDB client."""
    host = "localhost"
    port = 9200
    user = 'root'
    password = 'root'
    dbname = 'demo'
    protocol = 'line'

    client = DataFrameClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Write DataFrame")
    client.write_points(df, 'demo', protocol=protocol)

    print("Write DataFrame with Tags")
    client.write_points(df, 'demo',
                        {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

    print("Read DataFrame")
    client.query("select * from demo")

    print("Delete database: " + dbname)
    client.drop_database(dbname)

    return True
