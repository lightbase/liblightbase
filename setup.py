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
	  'ply == 3.6',
	  'decorator == 3.4.2',
          'requests == 2.7.0',
          'python-dateutil == 2.4.2',
          'six == 1.9.0',
          'jsonpath-rw == 1.4.0'
      ]
      )
