This a simple API for Canary that is built with Docker, Nginx, Flask, and Postgres.
The app works by first running Docker to build containers for the app/server/db.
Then using Docker to Initialize the wanted columns in the database and using Nginx
to serve the Flask APIS which can be scaled up for production. The API is a very simple
implementation that accepts POST/GET Calls.

## Usage

1. Initialize the Postgres Database in shell
$ docker-compose up -d db
$ docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

2. Bring up the cluster
$ docker-compose up -d

3. Bring online
$ docker-compose up

4. To scale up the number of workers, and to add to the number of available
connections for the api-change the 4 to a higher/lower number:
docker-compose up --scale flaskapp=4

5. The app runs at http://localhost:8080/ and API Calls can be directed there

## Making Calls

Expected Post Calls look like: {
"device_uuid": "b21ad0676f26439482cc9b1c7e827de4", "sensor_type": "temperature",
"sensor_value": 50.0,
"sensor_reading_time": 1510093202
}

While expected GET requests look like:
{ "sensor_type": "temperature", "start_time": 1510043401, "end_time": "1510043417", "device_uuid":"b21ad0676f26439482cc9b1c7e827de4" }


Both can be accessed at http://localhost:8080/ with Curl

POST:
curl -H "Content-Type: application/json" -X POST -d '{ "device_uuid": "b21ad0676f26439482cc9b1c7e827de4", "sensor_type": "temperature", "sensor_value": 70.0, "sensor_reading_time": 1510043411 }' http://localhost:8080/

GET:
curl -H "Content-Type:GET -d '{ "sensor_type": "temperature", "start_time": 1510043401, "end_time": "1510043414" }' http://localhost:8080/
