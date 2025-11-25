from setuptools import find_packages
from setuptools import setup

setup(
    name = 'file_forward',
    version = '0.0.0',
    packages = find_packages(),
    install_requires = [
        'passlib',
        'pymqi',
        'sqlalchemy',
        'sqlalchemy_utils',
    ],
)
