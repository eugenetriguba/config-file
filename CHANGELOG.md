# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

  - Add `reset()` and `save()` methods to `ConfigFile`. This allows you to reset your
    configuration file to an "original state," given the original config file path. 
    However, say you have a `config/config.json` file. Then it will automatically try 
    to look for `config/config.original.json` if no file path is specified. The `save()`
    method should be called after your changes to the config file. It will write them
    back out.
  - Raise test coverage to 93% (`BaseParser` is abstract so it isn't tested and some
    methods in `ConfigFile` simply use the same method in the parser so it doesn't make
    sense to test those methods.)

## 0.3.3

Fixed

  - `TypeError` when setting the key/value pairs since configparser requires the option 
   to be a string. The parser now just converts the value to a string if it is not one
   and then adds the key/value pair. It would still be parsed correctly when retrieving
   it.

## 0.3.3 - 2020-01-18 - 2020-01-17

Changed

  - `_split_on_dot` is no longer in base parser (now in a utils file). Also, the default 
  behavior is now to split on every dot and split on only the last dot if specified
  
Fixed

  - `ConfigFile` was trying to use `_split_on_dot`, but it no longer inherited from base parser.

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