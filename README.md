# Config File 

> Manage and manipulate your configuration files

[![Python 3.8.0|](https://img.shields.io/badge/python-3.8.0-blue.svg)](https://www.python.org/downloads/release/python-380/) 
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Build Status](https://travis-ci.com/eugenetriguba/config_file.svg?branch=master)](https://travis-ci.com/eugenetriguba/config_file)

> This python package is currently a work in progress and is in a pre-alpha phase. The API is liable to break until v1.

Config File allows you to use the same simple API for manipulating INI, JSON, 
YAML, and TOML configuration files. For the time being, it only supports INI.

## Installation
```bash
$ pip install config_file
```

## Examples

`config.ini`
```ini
[calendar]
today = monday
start_week_on_sunday = false
today_index = 0
quarter_hours_passed = 0.25
```

`example.py`
```python
from config_file import ConfigFile

config = ConfigFile("~/.config/test/config.ini")

# Output your config file as a string
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 0\nquarter_hours_passed = 0.25\n\n'

# Retrieve values with a section.key format
config.get("calendar.today")
>>> 'monday'

# Values from the config file are automatically parsed
config.get("calendar.start_week_on_sunday")
>>> False

# Values from the config file are automatically parsed
config.get("calendar.start_week_on_sunday")
>>> False

# Unless you don't want them to be parsed
config.get("calendar.today_index", parse_type=False)
>>> '0'

# The dot syntax is also used to set values. True is returned on success.
config.set("calendar.today_index", 20)
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'

# If you specify a section that isn't in your config file, the section and the key are added for you.
config.set("week.tuesday_index", 2)
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n[week]\ntuesday_index = 2\n\n'

# Delete can delete an entire section or just a key/value pair.
config.delete('week')
>>> True
config.stringify()
>>> '[calendar]\ntoday = monday\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'

# Delete can delete an entire section or just a key/value pair.
config.delete('calendar.today')
>>> True
config.stringify()
>>> '[calendar]\nstart_week_on_sunday = false\ntoday_index = 20\nquarter_hours_passed = 0.25\n\n'

# You can also just check if the file has a particular section or key.
config.has('calendar')
>>> True
config.has('week')
>>> False
config.has('calendar.start_week_on_sunday')
>>> True

# The file is only written back out when you call save()
config.save()
>>> True

# You can also reset the file back to its original state. The current configuration file 
# would be deleted and replaced by a copy of the original. By default, since our passed in
# config file was at path `~/.config/test/config.ini`, `reset()` will look for 
# `~/.config/test/config.original.ini`
config.reset()
>>> True

# Or you can specify the file path explicitly
config.reset(original_file_path="~/some_other_directory/this_is_actually_the_original.ini")
>>> True
```
