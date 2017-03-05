# Leider

A cli to manage services for apps in docker for local development.

## Services

PostgreSQL, Redis and RabbitMQ.

## Workflow

```
leider up [<service>[:<version>] ...]
leider down [<service>[:<version>] ...]
leider status
```

### Examples

```
$ leider up postgres redis rabbitmq
postgres: postgresql://my-app:f1783734bc641e80@localhost:32804/my-app
redis: redis://localhost:32805/0
rabbitmq: amqp://my-app:6b9fe90f0ad45f1c@localhost:32801/my-app

$ leider status
redis: running
postgres: running
rabbitmq: running

$ leider down
redis: exited
postgres: exited
rabbitmq: exited
```

Uses a config file to keep track of the containers.

```
$ cat my-app.cfg
[redis]
image = redis:3.0-alpine
id = 743d3fbb3cf3072bed42efd75b594004067c18a4697a3c0c13dd766c9454916b
short_id = 743d3fbb3c
name = infallible_davinci
host = localhost
port = 32805
redis_db = 0

[postgres]
image = postgres:9.6-alpine
id = 25d4085ca3b6843e37cfba96dd2cf85eabc3daefc6a163099881615109b35c75
short_id = 25d4085ca3
name = stoic_lumiere
host = localhost
port = 32804
db_name = my-app
db_user = my-app
db_pass = fc1ad03dfc37342c

[rabbitmq]
image = rabbitmq:3-alpine
id = 3baf171d2f10a27e8b8828fe621c5f364bf7d0a7846a832665985555a991002d
short_id = 3baf171d2f
name = condescending_bardeen
host = localhost
port = 32801
queue_vhost = my-app
queue_user = my-app
queue_pass = 4fdbf5c41e52eb90

```
