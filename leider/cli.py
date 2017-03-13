# -*- coding: utf-8 -*-
import sys

import click
import crayons

from .config import Config, InternalConfig
from .docker_utils import ensure_image_has_tag
from .services import ServiceTypes


internal_config = InternalConfig()
config = Config()


def emit_err(msg):
    """Print to stdout in red."""
    click.echo(crayons.red(msg), err=True)


def _ensure_image_is_valid(image):
    """Verifies that image is supported."""
    service_type = image
    if ':' in image:
        service_type = image.split(':')[0]
    return service_type in ServiceTypes.keys()


def ensure_config_is_valid(config):
    """Verifies that all services have a supported image."""
    config_error = False
    for service_name in config.all():
        service_conf = config.get(service_name)
        image = service_conf.get('image')
        if image is None:
            config_error = True
            emit_err("You need to specify an image for the service '{service_name}'.".format(
                service_name=service_name))
            continue
        image_is_valid = _ensure_image_is_valid(image)
        if not image_is_valid:
            config_error = True
            emit_err("The specified image ({image}) for '{service_name}' is not supported".format(
                service_name=service_name, image=image))
    if config_error:
        sys.exit(1)


def ensure_services_exist_in_config(config, service_names):
    """Verifies that services passed to cli exist in config."""
    config_error = False
    for service_name in service_names:
        if not config.has(service_name):
            config_error = True
            emit_err("'{service_name}' does not exist in Leider config.".format(
                service_name=service_name))
            continue
    if config_error:
        sys.exit(1)


def parse_image(image):
    """Spit out image name and version."""
    image_with_tag = ensure_image_has_tag(image)
    service_type = image_with_tag.split(':')[0]
    return service_type, image_with_tag


def init_service(service_name):
    """Initialize a service based on service name."""
    service_conf = config.get(service_name)
    service_type, image = parse_image(service_conf.get('image'))
    service_int_conf = internal_config.get(service_name)
    service = ServiceTypes.get(service_type)(service_name, image, service_int_conf)
    return service


@click.group()
@click.version_option()
def cli():
    """
    Leider manages services in Docker for all your local apps.
    """
    if not config.exists():
        emit_err("Leider config (leider.yaml) does not exist.")
        sys.exit(1)
    config.open()
    ensure_config_is_valid(config)


@click.command(help='Starts all or provided services. Prints out connection URLs.')
@click.argument('service_names', nargs=-1)
def up(service_names):
    ensure_services_exist_in_config(config, service_names)
    service_names = service_names or config.all()
    for service_name in service_names:
        service = init_service(service_name)
        service.up()
        click.echo('{}: {}'.format(service.name, service.url))
        internal_config.add_or_update(service)


@click.command(help='Stops all or provided services.')
@click.argument('service_names', nargs=-1)
def down(service_names):
    ensure_services_exist_in_config(config, service_names)
    service_names = service_names or config.all()
    for service_name in service_names:
        service = init_service(service_name)
        service.down()
        click.echo('{}: {}'.format(service_name, service.status))
        internal_config.add_or_update(service)


@click.command(help='Prints out the status of all services.')
def status():
    service_names = config.all()
    for service_name in service_names:
        service = init_service(service_name)
        click.echo('{}: {}'.format(service_name, service.status))


cli.add_command(up)
cli.add_command(down)
cli.add_command(status)
