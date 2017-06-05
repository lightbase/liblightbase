from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='liblightbase',
    version=version,
    description="LightBase Library",
    long_description="""\
LightBase Library""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='lightbase-neo ligthbase json database library',
    author='Lightbase',
    author_email='info@lightbase.com.br',
    url='http://lightbase.com.br/',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
    'voluptuous == 0.8.7',
    'ply == 3.4',
    'decorator == 3.4.0',
    'requests == 1.2.3',
    'python-dateutil == 2.2',
    'six == 1.7.2',
    'jsonpath-rw == 1.3.0'])
