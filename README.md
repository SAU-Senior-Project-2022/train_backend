# Train Backend

## Building
The simplest method to deploy this backend is to just use docker. Once `docker-compose` is installed on your server, just run `docker-compose up -d`, and on port 5000 you will have the webserver running. **TODO** CURRENTLY, port 27017 is also exposed, which is the mongodb port. This will be closed before the end of development, but, as mongodb doesn't have any authentication, should never be published beyond your firewall.

## Features in main.py
There are six options when launching main.py.

```
usage: main.py [-h] [--ip IP] [--port PORT] [--debug] [--http] [--cert-file CERT] [--key-file KEY]

Runs a server that provides the backend for trains.

options:
  -h, --help        show this help message and exit
  --ip IP           Specify the ip for the server. Default is 0.0.0.0.
  --port PORT       Specify the port for the server. Default is 5000.
  --debug           The server will be in debug mode
  --http            The server will run over http
  --cert-file CERT  Provide the path to the certificate file for the server. If not provided, it is provided by the server.
  --key-file KEY    Provide the path to the key file for the server. If not provided, it is provided by the server.
```

The main points are `--debug` and `--http`. By default, **the server is a development server**, but not in debug mode. This will need to change before publication. Also, if you don't want to put up with self signed certificates, you can use `--http` to use HTTP instead of HTTPS.

## Production
Once in production, you should specify with `--port` a different port that the default. Either `80` if using `--http`, or `443` if not. If using HTTPS, you can specify certificate and key files using `--cert-file` and `--key-file`.

# development
`docker-compose down` will destroy the containers, while `docker-compose stop` will just stop them. If changes are being made to the server, you should run `docker-compose down; docker build .; docker-compose up -d`, while if you are just stoping the service, you can just use `doker-compose stop`, and `docker-compose up -d` when you want to run the services again later.

If this directory is opened in `Visual Studio Code`, there are 3 debugger launch options currently. One to launch the webserver with HTTP, one for HTTPS, and one for launching the current python file.