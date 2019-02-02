"""pychess setup.py module."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychess",
    version="0.0.1",
    author="Dominik Niemiro",
    author_email="dniemiro@protonmail.com",
    description="Chess game implemented in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nieminik/pychess",
    packages=setuptools.find_packages(),
    classifiers=[

    ],
)
