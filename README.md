# Config File 

> Manage and manipulate your configuration files

[![Python 3.8.0|](https://img.shields.io/badge/python-3.8.0-blue.svg)](https://www.python.org/downloads/release/python-380/) 
[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)

> This python package is currently a work in progress and is in a pre-alpha phase. The API is liable to break until v1.

Config File allows you to use the same simple API for manipulating INI, JSON, 
YAML, and TOML configuration files. For the time being, it only supports INI.

## Motivation

With applications I was building, I found myself frequently having to use some sort of configuration folder with an object that modeled the configuration file. I did this to help more easily manipulate my configuration. However, I found myself needing this sort of thing for several different applications and would end up rewriting something similar. So ended up deciding to create a package out of it so I could focus more on the application I was building instead.

## Why not just use configparser, ConfigObj, etc.?

I wanted something a bit cleaner and simpler to use than configparser. The ini parser uses configparser under the hood, but it provides some niceties such as automatically parsing configuration values into their native types when you retrieve them. However, I also wanted something more flexible, and ini files aren't the only common configuration format. That is why Config File uses an adapter pattern to swap in and out the right parser for various file types you give it. This allows you to use the same API for all of your configuration needs. 

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
```
