#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
howdoi
===================
A Telegram bot
"""
from setuptools import setup, find_packages

install_requires = [
    'mock',
    'howdoi',
    'telepot>=8.3',
]


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
