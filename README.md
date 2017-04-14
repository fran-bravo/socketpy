# socketpy
[![Build Status](https://travis-ci.com/fran-bravo/socketpy.svg?token=xiwZKBqBy5Nsagz6fEGD&branch=master)](https://travis-ci.com/fran-bravo/socketpy)
[![Python Version](https://img.shields.io/badge/python-3.3%20%2B-blue.svg)](https://www.python.org/)

socketpy provides a CLI for the creation of basic models and packaging functions for data structures, used in sockets, in C.
It's interface helps avoid common boilerplater code used for sending structs with sockets.

## Installation
To install this package, first you need to have python 3.2 or higher in your operating system.

Check [Python](https://www.python.org/downloads/source/) for information about it's installation.

Once you have installed python 3, all you need to do is to use the command pip install socketpy and pip
will take care of the installation of the package.
## Usage
* Go to your project root directory.
* Run `socketpy config` and wait for it to configure. You might need to have root permissions for this command.
* Run `socketpy create socket` to create a directory for the headers and sources used.
* Run `socketpy create model name_model type_attribute:name_attribute ... `

#### Other commands

*   `help`: displays all available commands for socketpy or more information about a specific command.
*   `delete`: eliminates the sockets directory.
*   `deconfig`: deconfigs socketpy.
*   `flush`: deletes types from old projects on the db.
*   `reset`: resets socketpy db.
*   `route`: allows you to add a route to specific source and header files which will be used for type validation. `socketpy route /usr/include/commons`
*   `embed`: lets you add a specific data type and its associated source file. `socketpy embed t_log log.h`



## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
