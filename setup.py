#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="calculateur-moyenne",
    version="1.0.0",
    author="Sam",
    author_email="sam@example.com",
    description="Application Python pour calculer les moyennes scolaires avec Tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goldensam777/Calculateur-de-Moyennes",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
    ],
    python_requires=">=3.6",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "calculateur-moyenne=main:main",
        ],
    },
    include_package_data=True,
)
