# Train Backend

- [Train Backend](#train-backend)
  - [Building](#building)
  - [Features in main.py](#features-in-mainpy)
  - [Production](#production)
  - [Development](#development)
  - [Testing](#testing)
  - [Documentation and Station Registration](#documentation-and-station-registration)
  - [Requirements](#requirements)

## Building

The simplest method to deploy this backend is to just use docker. Once [docker-compose](https://docs.docker.com/compose/install/) is installed on your device, just run `docker-compose up -d`, and, on port 5000, you will have the webserver running.

## Features in [main.py](src/main.py)

There are many options when launching [`/src/main.py`](src/main.py), and too see them, Run `src/main.py -h`.

By default, **the server is a development server**, but not in debug mode, as this is currently a breaking option. If you don't want to put up with self signed certificates, you can use `--http` to use HTTP instead of HTTPS.

## Production

Once in production, you should specify with `--port` a different port that the default. Either `80` if using `--http`, or `443` if not. If using HTTPS, you can specify certificate and key files using `--cert-file` and `--key-file`.

## Development

`docker-compose down --rmi all` will destroy the containers, while `docker-compose down` will just stop them. If changes are being made to the server, you should run `docker-compose down --rmi all; docker-compose up -d`, while if you are just stoping the service, you can just use `doker-compose down`, and `docker-compose up -d` when you want to run the services again later.

If this directory is opened in [Visual Studio Code](https://code.visualstudio.com/), there are 3 debugger launch options currently. One to launch the webserver with HTTP, one for HTTPS, and one for launching the current python file

## Testing

If you wish to test the [server](src/main.py). You must run the server with the flag `--fresh` (You can add other flags if you need to be more specific) and run the [`server_test.py`](tests/server_test.py) application with the server loaded in order for the testing application to connect to the server. At the top of [`server_test.py`](tests/server_test.py) is the `URL` variable, which should be set to localhost to test localy, or the remote server, in our case [http://train.jpeckham.com:5000](http://train.jpeckham.com:5000).

## Documentation and Station Registration

If you wish to view the documentation, [click this link](http://train.jpeckham.com:5000/site/documentation).

If you wish to register a new "station", navigate to the [/site/location/new](http://train.jpeckham.com:5000/site/location/new) endpoint in a browser.

If you wish to register a new "state" for a station, navigate to the [/site/state/new](http://train.jpeckham.com:5000/site/state/new) endpoint in a browser.

## Requirements

The following document has a list of functional and nonfunctional requirements: [requirements.md](/requirements.md)
