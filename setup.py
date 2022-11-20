from __future__ import print_function

import sys

from setuptools import find_packages, setup

from pylti1p3 import __version__

if sys.version_info < (3, 6):
    error = "ERROR: PyLTI1p3 requires Python 3.6+ ... exiting."
    print(error, file=sys.stderr)
    sys.exit(1)


install_requires = [
    "jwcrypto",
    "pyjwt>=1.5",
    "requests",
    "typing_extensions",
]

with open("README.rst", "rt") as readme:
    long_description = readme.read().strip()

packages = find_packages(exclude=["examples", "tests"])

setup(
    name="PyLTI1p3",
    version=__version__,
    description="LTI 1.3 Advantage Tool implementation in Python",
    keywords="pylti,pylti1p3,lti,lti1.3,lti1p3,django,flask",
    author="Dmitry Viskov",
    author_email="dmitry.viskov@webenterprise.ru",
    maintainer="Dmitry Viskov",
    long_description=long_description,
    install_requires=install_requires,
    license="MIT",
    url="https://github.com/dmitry-viskov/pylti1.3",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={
        "pylti1p3": ["py.typed"],
        "pylti1p3.tool_config": ["py.typed"],
        "pylti1p3.contrib": ["py.typed"],
    },
)
