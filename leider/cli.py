# -*- coding: utf-8 -*-
import click

from .config import Config, InternalConfig
from .cli_utils import parse_image
from .services import get_service


@click.group()
@click.version_option()
def cli():
    """
    Leider manages services in Docker for all your local apps.
    """
    pass


@click.command(help='Starts all or provided services. Prints out connection URLs.')
@click.argument('service_names', nargs=-1)
def up(service_names):
    internal_config = InternalConfig()
    config = Config()
    service_names = service_names or config.all()
    for service_name in service_names:
        if not config.has(service_name):
            click.echo("'{service_name}' does not exist in 'leider.yaml'.".format(
                service_name=service_name))
            continue
        service_conf = config.get(service_name)
        image = service_conf.get('image')
        if image is None:
            click.echo("'{service_name}' does not have an image.".format(service_name=service_name))
            continue
        service_type, image = parse_image(image)
        service_int_conf = internal_config.get(service_name)
        service = get_service(service_type)(service_name, image, service_int_conf)
        service.up()
        click.echo('{}: {}'.format(service.name, service.url))
        internal_config.add_or_update(service)


@click.command(help='Stops all or provided services.')
@click.argument('service_names', nargs=-1)
def down(service_names):
    internal_config = InternalConfig()
    config = Config()
    service_names = service_names or config.all()
    for service_name in service_names:
        if not config.has(service_name):
            click.echo("'{service_name}' does not exist in 'leider.yaml'.".format(
                service_name=service_name))
            continue
        service_conf = config.get(service_name)
        image = service_conf.get('image')
        if image is None:
            click.echo("'{service_name}' does not have an image.".format(service_name=service_name))
            continue
        service_type, image = parse_image(image)
        service_int_conf = internal_config.get(service_name)
        service = get_service(service_type)(service_name, image, service_int_conf)
        service.down()
        click.echo('{}: {}'.format(service_name, service.status))
        internal_config.add_or_update(service)


@click.command(help='Prints out the status of all services.')
def status():
    internal_config = InternalConfig()
    config = Config()
    service_names = config.all()
    for service_name in service_names:
        if not config.has(service_name):
            click.echo("'{service_name}' does not exist in 'leider.yaml'.".format(
                service_name=service_name))
            continue
        service_conf = config.get(service_name)
        image = service_conf.get('image')
        if image is None:
            click.echo("'{service_name}' does not have an image.".format(service_name=service_name))
            continue
        service_type, image = parse_image(image)
        service_int_conf = internal_config.get(service_name)
        service = get_service(service_type)(service_name, image, service_int_conf)
        click.echo('{}: {}'.format(service_name, service.status))


cli.add_command(up)
cli.add_command(down)
cli.add_command(status)
