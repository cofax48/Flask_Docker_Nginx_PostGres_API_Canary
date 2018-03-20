import datetime
import os
#El Classico
from flask import Flask, abort
from flask import request
import json
from datetime import datetime
import time

#Gets db params
from models import DBConnect
from database import engine

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
conn = engine.connect()

@app.route("/", methods=('GET', 'POST'))
def POST_AND_GET():
    #If were sending a post call
    if request.method == 'POST':
        data = json.loads(request.data.decode())

        fields = [i for i in data]
        expected_fields = ["device_uuid", "sensor_type", "sensor_value", "sensor_reading_time"]
        approved_sensor_types = ["humidity", "temperature"]
        if expected_fields == fields:
            if str(data["sensor_type"]) in approved_sensor_types:
                if float(0.0) <= float(data["sensor_value"]) <= float(100.0):

                    #makes the id the timestamp, and making it to the microsecond makes it unique
                    dt = datetime.now()
                    id_inputted = float(str(time.time()) + str(dt.microsecond))

                    #Raw SQL Insertion
                    conn.execute('''INSERT INTO "Canary Sensor Data" VALUES ('{}', '{}', '{}', '{}', '{}');'''.format(\
                    id_inputted, data["device_uuid"], data["sensor_type"], data["sensor_value"], data["sensor_reading_time"]))
                    return json.dumps({"Success":"Success"}), 200, {'ContentType':'application/json'}

                #begin Error codes based on missing fields
                return abort(400)
            return abort(400)
        return abort(400)

    #If were sending a GET request then this code block runs
    if request.method == 'GET':

        data = json.loads(request.data.decode())
        fields = [i for i in data]
        expected_fields = ["sensor_type", "start_time", "end_time", "device_uuid"]
        approved_sensor_types = ["humidity", "temperature"]

        #checks to see if sent data fields match our expected parameters
        if expected_fields == fields:
            if str(data["sensor_type"]) in approved_sensor_types:

                #Raw SQL Query
                query = conn.execute('''SELECT * FROM "Canary Sensor Data" WHERE
                "Sensor_Reading_Time" >= '{}' AND "Sensor_Reading_Time" <= '{}'
                AND "Sensor_Type" = '{}' AND "device_uuid" = '{}';'''.format(\
                data["start_time"], data["end_time"], data["sensor_type"], data["device_uuid"]))
                processed_query = query.cursor.fetchall()

                #Builds the data ball to return formatted queries
                full_data_object_to_return = []
                for data_field in processed_query:
                    full_data_object_to_return.append({"device_uuid":data_field[1], \
                    "sensor_type":data_field[2], "sensor_value":data_field[3], \
                    "sensor_reading_time":data_field[4]})

                return json.dumps(full_data_object_to_return), 200, {'ContentType':'application/json'}

                #begin Error codes based on missing fields
                return abort(400)
            return abort(400)
    #returns if request is not "post/get"
    return abort(405)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
