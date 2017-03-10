# -*- coding: utf-8 -*-
import docker

client = docker.from_env()


def ensure_image_has_tag(image):
    image_with_tag = image
    if ':' not in image:
        image_with_tag = get_latest_version(image)
    return image_with_tag


def get_latest_version(images):
    return sorted(images, key=lambda i: i.tags[0], reverse=True)[0].tags[0]


def get_exposed_port(attrs, internal_port):
    tcp_port = '{}/tcp'.format(internal_port)
    return attrs['NetworkSettings']['Ports'][tcp_port][0]['HostPort']
