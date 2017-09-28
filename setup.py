#!/usr/bin/env python

from io import open
import os
from setuptools import setup, find_packages


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding='utf-8') as handle:
        return handle.read()


setup(
    name='django-shared-multilingual',
    version=__import__('multilingual').__version__,
    description=' Collection Django tools for multilingual websites.',
    long_description=read('README.md'),
    author='Erik Stein',
    author_email='erik@classlibrary.net',
    url='https://projects.c--y.net/erik/django-shared-multilingual/',
    license='MIT License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=['tests', 'tests.*'],
    ),
    include_package_data=True,
    install_requires=[
        # 'Django<2',
        'python-dateutil',
        'django-shared-utils',
    ],
    dependency_links=[
        'git+ssh://gogs@projects.c--y.net/erik/django-shared-utils.git#egg=django-shared-utils',
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    zip_safe=False,
    # tests_require=[
    #     'Django',
    #     # 'coverage',
    #     # 'django-mptt',
    #     # 'pytz',
    # ],
    # test_suite='main.runtests.runtests',
)
