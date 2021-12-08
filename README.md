# GeoAPI

- ### Django based app used to retrieve geolocation data based on given IP address.
- ### Allows retrieving, creating and deleting geolocation data
- ### Secured with JWT


## Tech stack
- Django
- Django Rest Framework
- PostgreSQL
- Docker

## Credentials

Example user:
```
{
  "username": "geoapi_user",
  "password": "password123"
}
```

## How to launch locally

1. Clone repository:

`$ git clone https://github.com/jakub-figat/geoapi`

2. In project root run:

`$ make build-dev`

3. In `config/.env` file, provide `access_key` from https://ipstack.com/

4. Start project

`$ make up-dev`

5. Load user from fixtures:

`$ make load-fixtures`

6. Go to `http://localhost:8000/api/swagger` to see SwaggerUI docs.

## Makefile
Project has `Makefile` with useful command aliases

## Tests
`$ make test`

Optionally with `location` param:

`$ make test location=tests.test_apps.test_geoapi`

## Live
API can be accessed at <aws_url>
