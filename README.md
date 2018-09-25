# Leider

A cli to manage services for apps in `Docker` for local development.

### Services

**PostgreSQL**, **Redis**, **Memcached** and **RabbitMQ**.

### Features

- Manages services in `Docker`.
- Exports connection URLs for your app.

### What is this good for?

- You don't have a Dockerized app (so `docker-compose` is not an option). Think `Heroku`, etc.
- You have some apps that need older versions of `PostgreSQL`, etc.

## Installation

```
$ pip install leider
```

or

```
$ pipsi install leider
```

## Usage

Create a `leider.yaml` in your app home. Example:

```
$ cat leider.yaml
db:
  image: postgres:9.6-alpine
cache:
  image: redis:3.0-alpine
queue:
  image: rabbitmq:3-alpine
```

Now you can start using the `Leider` cli.

```
$ leider
Usage: leider [OPTIONS] COMMAND [ARGS]...

  Leider manages services in Docker for all your local apps.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  down    Stops all or provided services.
  reset   Reset all or provided services.
  status  Prints out the status of all services.
  up      Starts all or provided services.
```


### Examples

```
$ leider up db cache queue
db: postgresql://leider-test:55df62e4e40da94a@localhost:32818/leider-test
cache: redis://localhost:32819/0
queue: amqp://leider-test:a212aa7457bfdcb4@localhost:32821/leider-test

$ leider status
db: running
cache: running
queue: running

$ leider down
db: exited
cache: exited
queue: exited
```

### Advanced

`Leider` keeps track of the `Docker` containers by storing a `yaml` file for each app in `~/.leider`.
