# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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
-  `IniParser` to support the ini format. It uses configparser internally, but it is 
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