#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
howdoi
===================
A Telegram bot
"""
from setuptools import setup, find_packages

install_requires = [
    'python-telegram-bot>=3.1.2',
    'mock>=1.3.0',
    'howdoi>=1.1.7',
    'PyYAML==3.11',
    'ndg-httpsclient>=0.4.0',
    'pyOpenSSL>=0.15.1',
]

tests_require = ['mock']


setup(
    name="HowDoIBot",
    version='0.1.0',
    author='Luiz Oliveira',
    author_email='ziuloliveira@gmail.com',
    url='https://github.com/Ziul/bot_howdoi',
    entry_points={
        'console_scripts': [
            'bot-run = main:main',
            'bot-test = main:test',
        ]},
    description='A Telegram bot',
    long_description=__doc__,
    license='GPLv3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
    test_suite="tests.run.runtests",
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3',
        'Topic :: Utilities',
    ],
)
