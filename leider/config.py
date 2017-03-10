# -*- coding: utf-8 -*-
import codecs
import os

import click
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap


class InternalConfig(object):

    def __init__(self):
        super(InternalConfig, self).__init__()
        self._app_dir = None
        self._filename = None
        self.ensure_config_exists()
        self.config = self._read()

    @property
    def app_dir(self):
        if self._app_dir is None:
            self._app_dir = click.get_app_dir('leider', force_posix=True)
        return self._app_dir

    @property
    def filename(self):
        if self._filename is None:
            self._filename = os.getcwd().split(os.sep)[-1] + '.yaml'
        return os.path.join(self.app_dir, self._filename)

    def ensure_app_dir_exists(self):
        if os.path.isdir(self.app_dir):
            pass
        elif os.path.isfile(self.app_dir):
            raise OSError("A file already exists at {0}.".format(self.app_dir))
        else:
            os.mkdir(self.app_dir)

    def ensure_config_exists(self):
        self.ensure_app_dir_exists()
        if not os.path.isfile(self.filename):
            cwd = os.getcwd()
            self.config = CommentedMap([
                ('project', cwd.split(os.sep)[-1]),
                ('path', cwd),
            ])
            self._write()

    def _read(self):
        with codecs.open(self.filename, 'r') as f:
            return ruamel.yaml.round_trip_load(f)

    def _write(self):
        with codecs.open(self.filename, 'w') as f:
            f.write(ruamel.yaml.round_trip_dump(self.config))

    def _ensure_services_key_exists(self):
        if 'services' not in self.config:
            self.config['services'] = CommentedMap([])

    def refresh(self):
        self.config = self._read()

    def add_or_update(self, service):
        self._ensure_services_key_exists()
        service_int_conf = CommentedMap([
            (field, getattr(service, field)) for field in service.config_fields()
        ])
        self.config['services'][service.name] = service_int_conf
        self._write()

    def get(self, service_name):
        self._ensure_services_key_exists()
        return self.config['services'].get(service_name, CommentedMap([]))


class Config(object):
    filename = 'leider.yaml'

    def __init__(self):
        self.config = self._read()

    def _read(self):
        with codecs.open(self.filename, 'r') as f:
            return ruamel.yaml.round_trip_load(f)

    def _write(self, conf):
        with codecs.open(self.filename, 'w') as f:
            f.write(ruamel.yaml.round_trip_dump(conf))

    def all(self):
        return self.config.keys()

    def has(self, service_name):
        return service_name in self.all()

    def get(self, service_name):
        return self.config.get(service_name)

    def add(self, service):
        if self.has(service.name):
            raise Exception('Service %r exists in %r' % (service.name, self.filename))
        self.config[service.name] = {'image': service.image}
        self._write(self.config)

    def remove(self, service_name):
        del self.config[service_name]
        self._write(self.config)
