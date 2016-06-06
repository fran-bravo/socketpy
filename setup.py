from setuptools import setup
from distutils.core import Extension

setup(
    name='socketpy',
    packages=['socketpy'],
    ext_modules=Extension('headers', sources=['modelos.h', 'paquetes.c', 'paquetes.h']),
    version='v0.0.6',
    description='First description for the module',
    author='Francisco Bravo',
    author_email='fran_ase@hotmail.com',
    license='MIT',
    url='https://github.com/fran-bravo/socketpy',
    download_url='https://github.com/fran-bravo/socketpy/tarball/v0.0.6',
    keywords=['sockets', 'C'],
    classifiers=['Development Status :: 3 - Alpha', ],
    entry_points={
        'console_scripts': [
            'socketpy = socketpy.__main__:main'
        ]
    },
)

