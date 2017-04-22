from setuptools import setup


setup(
    name='socketpy',
    packages=['socketpy'],
    version='v0.3.4',
    description='First description for the module',
    author='Francisco Bravo',
    author_email='fran_ase@hotmail.com',
    license='MIT',
    url='https://github.com/fran-bravo/socketpy',
    download_url='https://github.com/fran-bravo/socketpy/tarball/v0.3.4',
    keywords=['sockets', 'C'],
    classifiers=['Development Status :: 3 - Alpha', ],
    entry_points={
        'console_scripts': [
            'socketpy = socketpy.__main__:main'
        ]
    },
)

