from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='drsa.twitter',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='izhar@abyres.net',
      author_email='izhar@abyres.net',
      url='http://github.com/drsa/drsa.twitter',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['drsa'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'tweepy',
          'argh',
          'colored',
          'python-dateutil',
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
            'drsa-twitter=drsa.twitter.command:main',
        ]
      }
      )
