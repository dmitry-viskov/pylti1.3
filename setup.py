from __future__ import print_function

import os
import sys

from setuptools import setup, find_packages
from pylti1p3 import __version__

if sys.version_info < (2, 7):
    error = "ERROR: PyLTI1p3 requires Python 2.7+ ... exiting."
    print(error, file=sys.stderr)
    sys.exit(1)

setup(
    name='PyLTI1p3',
    version=__version__,
    description='LTI 1.3 implementation in Python',
    keywords="pylti,pylti1p3,lti,lti1.3,lti1p3,django",
    author='Dmitry Viskov',
    author_email='dmitry.viskov@webenterprise.ru',
    maintainer="Dmitry Viskov",
    long_description="\n\n".join([
        open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    ]),
    install_requires=[
        'pyjwt>=1.5',
        'jwcrypto',
        'requests'
    ],
    license='Apache Software License 2.0',
    url='https://github.com/dmitry-viskov/pylti1.3',
    packages=find_packages(exclude=["examples"]),
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
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
