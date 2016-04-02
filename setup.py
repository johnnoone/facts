#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

with open('README.rst') as file:
    content = file.read()

setup(
    name='facts',
    version=versioneer.get_version(),
    description='Return facts of server',
    long_description=content,
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    url='https://github.com/johnnoone/facts',
    packages=find_packages(),
    keywords=[
        'infrastructure',
        'asyncio',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Clustering',
    ],
    install_requires=[
        'aioutils',
        'netifaces',
        'PyYAML',
        'psutil',
        'uptime',
    ],
    extras_require={
        ':python_version=="3.3"': ['asyncio'],
    },
    entry_points={
        'console_scripts': [
            'facts = facts.__main__:run'
        ],
        'facts.graft': [
            'ruby-facts = facts.contribs:facter_info'
        ]
    },
    cmdclass=versioneer.get_cmdclass()
)
