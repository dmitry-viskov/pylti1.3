from __future__ import print_function

import sys

from setuptools import setup, find_packages
from pylti1p3 import __version__

if sys.version_info < (2, 7):
    error = "ERROR: PyLTI1p3 requires Python 2.7+ ... exiting."
    print(error, file=sys.stderr)
    sys.exit(1)

with open("README.rst", "rt") as readme:
    long_description = readme.read().strip()

setup(
    name='PyLTI1p3',
    version=__version__,
    description='LTI 1.3 Advantage Tool implementation in Python',
    keywords="pylti,pylti1p3,lti,lti1.3,lti1p3,django",
    author='Dmitry Viskov',
    author_email='dmitry.viskov@webenterprise.ru',
    maintainer="Dmitry Viskov",
    long_description=long_description,
    install_requires=[
        'pyjwt>=1.5',
        'jwcrypto',
        'requests'
    ],
    license='MIT',
    url='https://github.com/dmitry-viskov/pylti1.3',
    packages=find_packages(exclude=["examples", "tests"]),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
