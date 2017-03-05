# -*- coding: utf-8 -*-
import click

from .config import Config
from .docker_utils import get_image
from .services import get_service


@click.group()
@click.version_option()
def cli():
    """
    Leider manages services in Docker for all your local apps.
    """
    pass


@cli.command()
@click.argument('services', nargs=-1)
def up(services):
    config = Config.read()
    services_info = {}
    services = services or config.sections()
    for service_name in services:
        service_conf = {}
        if config.has_section(service_name):
            service_conf = dict(config.items(service_name))
        image = service_conf.get('image', get_image(service_name))
        service = get_service(service_name)('localhost', image, service_conf)
        service.up()
        click.echo('{}: {}'.format(service_name, service.url))
        services_info[service_name] = service
    if services_info:
        Config.write(services_info)


@cli.command()
@click.argument('services', nargs=-1)
def down(services):
    config = Config.read()
    services_info = {}
    services = services or config.sections()
    for service_name in services:
        section = {}
        if config.has_section(service_name):
            section = dict(config.items(service_name))
        image = section.get('image')
        service = get_service(service_name)('localhost', image, section)
        service.down()
        click.echo('{}: {}'.format(service_name, service.status))
        services_info[service_name] = service
    if services_info:
        Config.write(services_info)


@cli.command()
def status():
    config = Config.read()
    for service_name in config.sections():
        section = dict(config.items(service_name))
        image = section.get('image')
        service = get_service(service_name)('localhost', image, section)
        click.echo('{}: {}'.format(service_name, service.status))
