# -*- coding: utf-8 -*-
import os

from .docker_utils import client, get_exposed_port


def get_service(service_name):
    try:
        return SERVICES[service_name]
    except KeyError:
        return None


class Service(object):
    internal_port = None

    def __init__(self, name, image, config):
        super(Service, self).__init__()
        self._container = None
        self._attrs = None
        self._port = None
        self._short_id = None

        self.name = name
        self.id = config.get('id', None)
        self.host = 'localhost'
        self.image = image

    @property
    def container(self):
        if self.id is not None and self._container is None:
            self._container = client.containers.get(self.id)
        return self._container

    @property
    def attrs(self):
        if self.id is not None and self._attrs is None:
            self._attrs = self.container.attrs
        return self._attrs

    @property
    def port(self):
        if self.status == 'running':
            self._port = get_exposed_port(self.attrs, self.internal_port)
        return self._port

    @property
    def status(self):
        if self.container:
            return self.container.status
        return 'does not exist'

    def config_fields(self):
        return ('image', 'id', 'host', 'port')

    def up(self):
        container = self.container
        if container is None:
            container = self.run()
        else:
            container.start()
        self._container = None
        self.id = container.id

    def down(self):
        if self.container:
            self.container.stop()
        self._container = None


class PostgreSQL(Service):
    internal_port = 5432

    def __init__(self, name, image, config):
        super(PostgreSQL, self).__init__(name, image, config)
        self.db_name = config.get('db_name', os.getcwd().split(os.sep)[-1])
        self.db_user = config.get('db_user', self.db_name)
        self.db_pass = config.get('db_pass', os.urandom(8).encode('hex'))

    def config_fields(self):
        base_fields = super(PostgreSQL, self).config_fields()
        return base_fields + ('db_name', 'db_user', 'db_pass')

    def run(self):
        container = client.containers.run(
            image=self.image,
            detach=True,
            publish_all_ports=True,
            environment={
                'POSTGRES_DB': self.db_name,
                'POSTGRES_USER': self.db_user,
                'POSTGRES_PASSWORD': self.db_pass,
            },
        )
        return container

    @property
    def url(self):
        return 'postgresql://{user}:{pswd}@{host}:{port}/{name}'.format(
            host=self.host,
            port=self.port,
            name=self.db_name,
            user=self.db_user,
            pswd=self.db_pass,
        )


class Redis(Service):
    internal_port = 6379

    def __init__(self, name, image, config):
        super(Redis, self).__init__(name, image, config)
        self.redis_db = config.get('redis_db', 0)

    def config_fields(self):
        base_fields = super(Redis, self).config_fields()
        return base_fields + ('redis_db', )

    def run(self):
        container = client.containers.run(
            image=self.image,
            detach=True,
            publish_all_ports=True,
        )
        return container

    @property
    def url(self):
        return 'redis://{host}:{port}/{db}'.format(
            host=self.host,
            port=self.port,
            db=self.redis_db,
        )


class Memcached(Service):
    internal_port = 11211

    def __init__(self, name, image, config):
        super(Memcached, self).__init__(name, image, config)

    def run(self):
        container = client.containers.run(
            image=self.image,
            detach=True,
            publish_all_ports=True,
        )
        return container

    @property
    def url(self):
        return 'memcached://{host}:{port}'.format(
            host=self.host,
            port=self.port,
        )


class RabbitMQ(Service):
    internal_port = 5672

    def __init__(self, name, image, config):
        super(RabbitMQ, self).__init__(name, image, config)
        self.queue_vhost = config.get('queue_vhost', os.getcwd().split(os.sep)[-1])
        self.queue_user = config.get('queue_user', self.queue_vhost)
        self.queue_pass = config.get('queue_pass', os.urandom(8).encode('hex'))

    def config_fields(self):
        base_fields = super(RabbitMQ, self).config_fields()
        return base_fields + ('queue_vhost', 'queue_user', 'queue_pass')

    def run(self):
        container = client.containers.run(
            image=self.image,
            detach=True,
            publish_all_ports=True,
            environment={
                'RABBITMQ_DEFAULT_VHOST': self.queue_vhost,
                'RABBITMQ_DEFAULT_USER': self.queue_user,
                'RABBITMQ_DEFAULT_PASS': self.queue_pass,
            },
        )
        return container

    @property
    def url(self):
        return 'amqp://{user}:{pswd}@{host}:{port}/{vhost}'.format(
            host=self.host,
            port=self.port,
            vhost=self.queue_vhost,
            user=self.queue_user,
            pswd=self.queue_pass,
        )


SERVICES = {
    'postgres': PostgreSQL,
    'redis': Redis,
    'memcached': Memcached,
    'rabbitmq': RabbitMQ,
}
