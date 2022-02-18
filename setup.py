"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pcal6524_i2c",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Python i2c library for pcal6524 gpio extender",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project's main homepage.
    url="https://github.com/rchavira/pcal6524_i2c",
    # Author details
    author="Ricardo Chavira",
    author_email="",
    install_requires=["smbus2"],
    # Choose your license
    license="GPLv3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: GPUv3 License",
        "Programming Language :: Python :: 3",
    ],
    # What does your project relate to?
    keywords="adafruit max31855 thermocouple hardware micropython circuitpython",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    py_modules=["PCAL6524", "i2c_device"],
)
