# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.8.0 - 2020-02-02

Added

  - More type hints to `ConfigFile` and `IniParser`.
  - `nested_lookup` dependency to help with modifying deeply nested structures 
    (JSON + YAML)
  - `JsonParser` so you can now specify `.json` files to be parsed.
  
Changed

  - The original content of the passed in file is now called `content` 
    instead of `contents`. This is for consistency since the parsed version is
    called `parsed_content`.

## 0.7.0 - 2020-01-27

Fixed

  - Support for using custom parsers with `ConfigFile` with the `parser` optional 
    argument. This was technically supported before, but it was not tested and found
    to not actually use the passed in parser once tested.

Changed

  - The `reset()` method on `ConfigFile` is now called `restore_original()`. 
    The behavior is the same. This was done to better describe what exactly that method
    is doing. Since the file is not written back out with every `set()` or `delete()`
    and calling `save()` explicitly is required, `reset()` may have been confused with
    resetting the changes you've made rather than deleting and restoring the original
    configuration file.

## 0.6.0 - 2020-01-24

Changed

  - Bumped down python version requirement to 3.6 and now test 3.6, 3.7, and 3.8 on CI.

## 0.5.0 - 2020-01-19

Added

  - Support for retrieving entire sections as a `dict` with `get()`. 

## 0.4.0 - 2020-01-19

Added

  - `reset()` and `save()` methods to `ConfigFile`. This allows you to reset your
    configuration file to an "original state," given the original config file path. 
    However, say you have a `config/config.json` file. Then it will automatically try 
    to look for `config/config.original.json` if no file path is specified. The `save()`
    method should be called after your changes to the config file. It will write them
    back out.
    
  - Raise test coverage to 93%.

## 0.3.3 - 2020-01-18

Changed

  - `_split_on_dot` is no longer in base parser (now in a utils file). Also, the default 
  behavior is now to split on every dot and split on only the last dot if specified
  
Fixed

  - `ConfigFile` was trying to use `_split_on_dot`, but it no longer inherited from base parser.
  
  - `TypeError` when setting the key/value pairs since configparser requires the option 
    to be a string. The parser now just converts the value to a string if it is not one
    and then adds the key/value pair. It would still be parsed correctly when retrieving
    it.

## 0.3.1 - 2020-01-17

Fixed

  - `isinstance` call for `BaseParser` to be correctly used.

## 0.3.0 - 2020-01-17

Added

  - Abstract base parser as a contract for concrete file format parser implementations.
  
  - Exposed `ConfigFile`, `BaseParser`, and `ParsingError` to the Public API. The base
  parser is exposed to allow future custom extensions of the config file and what it 
  can parse by its users.
  
  - `has_section` and `has_key` is now changed to a single `has` method which determines
    whether you're checking a section or key by the presence of a dot.
    
  - `IniParser` to support the ini format. It uses configparser internally, but it is 
    only exposed through the `ConfigFile` object. 

## 0.2.0 - 2020-01-04

Added

  - Parsing of strings to their native values

## 0.1.0 - 2020-01-04

Added

  - Created the config_file package with only the version inside it
  
  - toml and pyyaml to dependencies
  
  - Pre-commit pipeline with autoflake, isort, black, and flake8
  
  - MIT license
  
  - Contributing guidelines
  
  - bump2version for easily upgrading versions of config file
  
  - pytest to dev dependencies for testing later on
