# Config File 

> Manage and manipulate your configuration files

![Python Verisons](https://img.shields.io/pypi/pyversions/config-file.svg)
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Documentation Status](https://readthedocs.org/projects/config-file/badge/?version=latest)](https://config-file.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/eugenetriguba/config_file.svg?branch=master)](https://travis-ci.com/eugenetriguba/config_file)
[![Codecov](https://codecov.io/gh/eugenetriguba/config_file/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/config_file)

> This python package is currently in rapid development and is in a pre-alpha phase. 
> The API is liable to break until v1 so if you're going to use it, pinning the version
> is recommended. All notable changes are kept track of in the changelog. 

Config File allows you to use the same simple API for manipulating INI, JSON, 
YAML, and TOML configuration files. For the time being, it only supports INI and
JSON. 

## Installation
```bash
$ pip install config-file
```

## Example

The `config_file` package exposes `ConfigFile`, `ParsingError`, and `BaseParser` to the public API.

### Sample Configuration File

`config.ini`
```ini
[calendar]
today = monday
start_week_on_sunday = false
today_index = 0
quarter_hours_passed = 0.25
```

### Create a ConfigFile
```python
from config_file import ConfigFile

config = ConfigFile("~/.config/test/config.ini")
```

### Output your config file as a string
```python
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 0\nquarter_hours_passed = 0.25\n\n'
```

### Retrieve values or sections
A section.key format is used for retrieving and setting values.
```python
# Values from the config file are automatically parsed
config.get("calendar.start_week_on_sunday")
>>> False

# Unless you don't want them to be parsed
config.get("calendar.start_week_on_sunday", parse_type=False)
>>> 'false'

config.get("calendar")
>>> {'today': 'monday', 'start_week_on_sunday': False, 'today_index': 0, 'quarter_hours_passed': 0.25}
```

### Set values
```python
config.set("calendar.today_index", 20)
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'

# If you specify a section that isn't in your config file, the section and the key are added for you.
config.set("week.tuesday_index", 2)
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n[week]\ntuesday_index = 2\n\n'
```

### Delete sections or key/value pairs.
```python
config.delete('week')
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'

config.delete('calendar.today')
>>> True
config.stringify()
>>> '[calendar]\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'
```


### Check whether you have a particular section or key
```python
config.has('calendar')
>>> True

config.has('week')
>>> False

config.has('calendar.start_week_on_sunday')
>>> True
```

### Save when you're done
Write the contents of the file back out. `set()` and `delete()` both modify the contents 
of the file and require a call to `save()` to write those changes back out.
```python
config.save()
>>> True
```

### Restore the file back to its original 

The current configuration file would be deleted and replaced by a copy of the original. 
By default, since our passed in config file was at path `~/.config/test/config.ini`, 
`restore_original()` will look for `~/.config/test/config.original.ini`.

```python
config.restore_original()
>>> True

# But you can also specify the original config file explicitly.
config.restore_original(original_file_path="~/some_other_directory/this_is_actually_the_original.ini")
>>> True
```

## Using your own parser

You can still use config file, even if you don't use one of our supported configuration 
formats. The `ConfigFile` object swaps in the parser it needs based on the file format. 
However, the constructor takes in an optional `parser` argument that you can use to 
supply your own custom parser. The only requirement is that the parser must be a 
concrete implementation of `BaseParser`. 
