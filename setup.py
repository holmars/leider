#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="leider",
    version="0.2.2",
    description="Manages services in Docker for all your local apps.",
    author="Hólmar Sigmundsson",
    author_email="holmars@gmail.com",
    url="https://github.com/holmars/leider",
    packages=["leider"],
    entry_points={"console_scripts": ["leider=leider:cli"]},
    install_requires=["click", "crayons", "docker", "ruamel.yaml<0.15"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
