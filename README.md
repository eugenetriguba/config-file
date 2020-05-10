# Config File

> Manage and manipulate your configuration files

![Python Version](https://img.shields.io/pypi/pyversions/config-file.svg)
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Documentation Status](https://readthedocs.org/projects/config-file/badge/?version=latest)](https://config-file.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/eugenetriguba/config-file.svg?branch=master)](https://travis-ci.com/eugenetriguba/config-file)
[![Codecov](https://codecov.io/gh/eugenetriguba/config-file/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/config-file)

## About Config File

The Config File project is designed to allow you to easily manipulate your 
configuration files with the same simple API. for manipulating INI,
JSON, YAML, and TOML configuration files. For the time being, it only
supports INI and JSON.

## Installation

Config File is available to download through PyPI using pip.

```bash
$ pip install config-file
```

If you want to manipulate YAML and TOML, you'll want to download the extras as well.

```bash
$ pip install config-file[yaml, toml]
```

## Usage

Say you have an INI file you want to manipulate. It must have an .ini
extension in order for the package to recognize it.

```ini
[section]
first_key = 5
second_key = blah
third_key = true
```

Then we can manipulate it as follows.

```python
from config_file import ConfigFile

ORIGINAL_CONFIG_PATH = Path("~/some-project/some-other-config-file.ini")
CONFIG_PATH = Path("~/some-project/config.ini")

# Our path can be a string or a Path object. 
# The "~" will be automatically expanded to the full path for us.
config = ConfigFile(CONFIG_PATH)

# All the types will be retrieved as strings unless specified otherwise.
print(config.get("section.first_key"))
>>> "5"
print(config.get("section.first_key", return_type=int))
>>> 5

# This holds true when we retrieve entire sections as well. However, we can
# also recursively parse the entire section is desired.
print(config.get("section"))
>>> {'first_key': '5', 'second_key': 'blah', 'third_key': 'true'}
print(config.get("section", parse_types=True))
>>> {'first_key': 5, 'second_key': 'blah', 'third_key': True}

# Sometimes we want to retrieve a key but don't know whether or not 
# it will be set. In that case, we can set a default.
print(config.get("section.unknown", default=False))
>>> False

# Setting, deleting, and checking if a key exists is just as easy.
print(config.set("section.first_key", 10))
>>> True

print(config.delete("section.third_key"))
>>> True

print(config.has("section.third_key"))
>>> False

# We can also convert the entire configuration file to a string.
print(config.stringify())
>>> '[section]\nfirst_key = 5\nsecond_key = blah\nthird_key = true\n\n'

# Lastly, we need to make sure we save our changes. Nothing is written
# out until we do so.
print(config.save())
>>> True

# If we have, say, a default config file and a user config file, we can easily
# restore default one. We can specify the file path to it.
print(config.restore_original(original_file_path=ORIGINAL_CONFIG_PATH))
>>> True

# Otherwise, a config.original.ini file will automatically be looked for in the
# current directory (because our configuration file we passed in was 
# named config.ini).
print(config.restore_original())
>>> True
```

##  Documentation

Full documentation and API reference is available at https://config-file.readthedocs.io

## License

The [MIT](https://github.com/eugenetriguba/config-file/blob/master/LICENSE) License.