from setuptools import setup, find_packages
from os import path

setup(
    name = 'pygl',
    version = '0.1',
    description = 'Attempt at a more pythonic OpenGL binding',
    author = 'Daniel Roberts',
    author_email = 'Ademan555@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'}
     )
