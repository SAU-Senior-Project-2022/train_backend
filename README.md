# Train Backend

- [Train Backend](#train-backend)
  - [Building](#building)
  - [Features in main.py](#features-in-mainpy)
  - [Production](#production)
  - [Development](#development)
  - [Testing](#testing)

## Building

The simplest method to deploy this backend is to just use docker. Once [`docker-compose`](https://docs.docker.com/compose/install/) is installed on your device, just run `docker-compose up -d`, and on port 5000 you will have the webserver running.

## Features in main.py

There are many options when launching main.py. Run `main.py -h` to see all options.

A couple main flags are `--debug` and `--http`. By default, **the server is a development server**, but not in debug mode. Also, if you don't want to put up with self signed certificates, you can use `--http` to use HTTP instead of HTTPS. The default configuration is to look for a database on `localhost` with username `root` and no password. This is likely not your configuration, but if run through docker, will all be setup properly.

## Production

Once in production, you should specify with `--port` a different port that the default. Either `80` if using `--http`, or `443` if not. If using HTTPS, you can specify certificate and key files using `--cert-file` and `--key-file`.

## Development

`docker-compose down` will destroy the containers, while `docker-compose stop` will just stop them. If changes are being made to the server, you should run `docker-compose down; docker build .; docker-compose up -d`, while if you are just stoping the service, you can just use `doker-compose stop`, and `docker-compose up -d` when you want to run the services again later.

If you wish to just run one of the images provided by the [`docker-compose.yml`](/docker-compose.yml), you can run either `docker-compose up -d --no-deps --build flask` or `docker-compose up -d --no-deps --build mariadb`, and the specified image will be run.

If this directory is opened in `Visual Studio Code`, there are 3 debugger launch options currently. One to launch the webserver with HTTP, one for HTTPS, and one for launching the current python file

## Testing

If you wish to test the [server](src/main.py). You must run the server with the flags `--debug`, `--fresh`, `--seed` (You can add other flags if you need to be more specific) and run the [`server_test.py`](tests/server_test.py) application with the server loaded in order for the testing application to connect to the server.
