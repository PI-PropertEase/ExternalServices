# External Services

Simulation of external services that integrate with PropertEase application.

## How to run:

While at the `ExternalServices/apis/` directory, run:

`uvicorn api_xxxx.main:app --reload`

Where "xxxxx" is the api name. Example:

`uvicorn api_zooking.main:app --reload --host 0.0.0.0`

`uvicorn api_earthstayin.main:app --reload --host 0.0.0.0 --port 8001`

`uvicorn api_clickandgo.main:app --reload --host 0.0.0.0 --port 8002`

## Docs (Swagger):

http://127.0.0.1:8000/docs#/
