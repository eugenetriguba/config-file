# Config File

> Modify configuration files of various formats with the same simple API

![Python Version](https://img.shields.io/pypi/pyversions/config-file.svg)
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Documentation Status](https://readthedocs.org/projects/config-file/badge/?version=latest)](https://config-file.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/eugenetriguba/config-file/workflows/python%20package%20CI/badge.svg?branch=master)](https://github.com/eugenetriguba/config-file/actions/)
[![Codecov](https://codecov.io/gh/eugenetriguba/config-file/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/config-file)

## About Config File

The Config File project is designed to allow you to easily manipulate your
configuration files with the same simple API whether they are in INI, JSON,
YAML, or TOML.

The code for this package grew origically out of developing command
line tools in Python. I had felt like I was writing similar code over and over
again to abstract away Python's configparser so it was a little nicer to work with
for my uses. Therefore, I had ended up making a package out of it and adding a lot more
niceties, polish, and flexibility to it so others may find it useful as well.

## Installation

Config File is available to download through PyPI.

```bash
$ pip install config-file
```

### Installing Extras

If you want to manipulate YAML and TOML, you'll want to download the extras as well.

```bash
$ pip install config-file[yaml, toml]
```

You can also use [Poetry](https://python-poetry.org).

```bash
$ poetry install config-file -E yaml -E toml
```

## Usage Overview

For this overview, let's say you have the following `ini` file
you want to manipulate.

```ini
[section]
num_key = 5
str_key = blah
bool_key = true
list_key = [1, 2]

[second_section]
dict_key = { "another_num": 5 }
```

It must have a `.ini` extension in order
for the package to recognize it and use the correct parser for it.

### Setting up ConfigFile

To use the package, we import in the `ConfigFile` object.

We can set it up by giving it a string or `pathlib.Path` as the argument.
Any home tildes `~` in the string or `Path` are recognzied and converted
to the full path for us.

```python
from config_file import ConfigFile

config = ConfigFile("~/some-project/config.ini")
```

### Using `get()`

A recurring pattern you'll see here is that all methods that
need to specify something inside your configuration file will
do so using a dot syntax.

#### Retrieving keys and sections

So to retrieve our `num_key`, we'd specify the heading and the
key separated by a dot. All values will then be retrieved as
strings.

```python
config.get('section.num_key')
>>> '5'
```

While we can retrieves keys, we can also retrieve the entire
section, which will be returned back to us as a dictionary.

```python
config.get('section')
>>> {'num_key': '5', 'str_key': 'blah', 'bool_key': 'true', 'list_key': '[1, 2]'}
```

#### Coercing the return types

However, some of these keys are obviously not strings natively.
If we are retrieving a particular value of a key, we may want to
coerce it right away without doing clunky type conversions after
each time we retrieve a value. To do this, we can utilize the
`return_type` keyword argument.

```python
config.get('section.num_key', return_type=int)
>>> 5
```

Sometimes we don't have structures quite that simple though. What
if we wanted all the values in `section` coerced? For that, we can
utilize a `parse_types` keyword argument.

```python
config.get('section', parse_types=True)
>>> {'num_key': 5, 'str_key': 'blah', 'bool_key': True, 'list_key': [1, 2]}
```

It also works for regular keys.

```python
config.get('section.num_key', parse_types=True)
>>> 5
```

#### Handling non-existent keys

Sometimes we want to retrieve a key but are unsure of if it will exist.
There are two ways we could handle that.

The first is the one we're used to seeing: catch the error.

```python
from config_file import MissingKeyError

try:
    important_value = config.get('section.i_do_not_exist')
except MissingKeyError:
    important_value = 42
```

However, the `get` method comes with a `default` keyword argument that we
can utilze for this purpose.

```python
config.get('section.i_do_not_exist', default=42)
>>> 42
```

This can be handy if you have a default for a particular configuration value.

### Using `set()`

We can use `set()` to set a existing key's value.

```python
config.set('section.num_key', 6)
```

The method does not return anything, since there is nothing
useful to return.



# Setting, deleting, and checking if a key exists is just as easy.
config.set("section.first_key", 10)
config.delete("section.third_key")

print(config.has("section.third_key"))
>>> False

# We can also convert the entire configuration file to a string.
print(config.stringify())
>>> '[section]\nfirst_key = 10\nsecond_key = blah\n\n'

# Lastly, we need to make sure we save our changes.
# Nothing is written out until we do so.
config.save()

# If we have, say, a default config file and a user config file, we can easily
# restore default one. We can specify the file path to it.
config.restore_original(original_file_path=ORIGINAL_CONFIG_PATH)

# Otherwise, a config.original.ini file will automatically be looked for in the
# current directory (because our configuration file we passed in was
# named config.ini).
config.restore_original()
```

## Documentation

Full documentation and API reference is available at https://config-file.readthedocs.io

## License

The [MIT](https://github.com/eugenetriguba/config-file/blob/master/LICENSE) License.
