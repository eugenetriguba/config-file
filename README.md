# Config File 

> Manage and manipulate your configuration files

[![Python 3.8.0|](https://img.shields.io/badge/python-3.8.0-blue.svg)](https://www.python.org/downloads/release/python-380/) 
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Build Status](https://travis-ci.com/eugenetriguba/config_file.svg?branch=master)](https://travis-ci.com/eugenetriguba/config_file)
[![Codecov](https://codecov.io/gh/eugenetriguba/config_file/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/config_file)

> This python package is currently a work in progress and is in a pre-alpha phase. The API is liable to break until v1.

Config File allows you to use the same simple API for manipulating INI, JSON, 
YAML, and TOML configuration files. For the time being, it only supports INI.

## Installation
```bash
$ pip install config_file
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
The contents are only written back out when you call `save()`.
```python
config.save()
>>> True
```

### Reset the file back to its original 

The current configuration file would be deleted and replaced by a copy of the original. 
By default, since our passed in config file was at path `~/.config/test/config.ini`, `reset()` 
will look for `~/.config/test/config.original.ini`.

```python
config.reset()
>>> True

# But you can also specify the original config file explicitly.
config.reset(original_file_path="~/some_other_directory/this_is_actually_the_original.ini")
>>> True
```

## Using your own parser

> This feature is a work in-progress and has not been tested yet.

You can still use config file, even if you don't use one of our supported configuration formats. The `ConfigFile` object swaps in the parser it needs based on the file format. However, the constructor takes in an optional `parser` argument that you can use to supply your own custom parser. The only requirement is that the parser must be a concrete implementation of `BaseParser`. 
