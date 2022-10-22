# Mini-microservices-docker-rabbitmq-system

## Table Of Content

- [Description](#Description)
- [Running the service](#Running-the-service)
    - [Using PDM](#Using-PDM)
    - [Using Makefile](#Using-makefile)

## Description

This's a mini docker based system containing 3 modules:

1. password_module: search inside a folder - "theHarvester", which contains multiple files and folders and try to
   extract a password contained in one of them.
2. analyze_module: analyze the files as so:
    1. Find the number of files from each type (e.g. .py, .txt, etc...)
    2. List the top 10 files by size sorted.
3. controller_module: executes the other modules and output the results into a json file.

> NOTE:
> - The communication between the controller and the module are conducted through a message broker(RabbitMQ).
> - There is no communication between the analyze_module and password_modules as they are not sharing the same networks.
> - "theHarvester" folder's available to the password and analyze modules containers by volumes.

## Running the service

clone the repo `git clone git@github.com:Refaelbenzvi24/Mini-microservices-docker-rabbitmq-system.git`

then

```shell
cd Mini-microservices-docker-rabbitmq-system
```

### Using [PDM](https://pdm.fming.dev/latest/):

```shell
pdm run docker:up
```

### Using makefile:

Since PDM is not well known for the time being, I have generated a makefile, just run the following:

```shell
make docker-up
```

> Note: The json output file destination directory is at: "./controller_module/output/result.json"