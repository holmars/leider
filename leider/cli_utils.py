# -*- coding: utf-8 -*-
from .docker_utils import ensure_image_has_tag


def parse_image(image):
    image_with_tag = ensure_image_has_tag(image)
    service_type = image_with_tag.split(':')[0]
    return service_type, image_with_tag
