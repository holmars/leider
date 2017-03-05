# -*- coding: utf-8 -*-
import ConfigParser


class Config(object):
    filename = 'leider.cfg'

    @staticmethod
    def read():
        config = ConfigParser.RawConfigParser()
        config.read(Config.filename)
        return config

    @staticmethod
    def write(services):
        config = ConfigParser.RawConfigParser()

        for name, service in services.iteritems():
            config.add_section(name)
            for field in service.config_fields():
                config.set(name, field, getattr(service, field))

        with open(Config.filename, 'wb') as configfile:
            config.write(configfile)
