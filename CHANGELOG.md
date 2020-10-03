# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.12.0 - 2020-10-03

### Added

  - Python's built-in `in` keyword now works with a ConfigFile.

    Example:
    ```python
    config = ConfigFile('./pyproject.toml')

    'tool.poetry' in config
    >>> True
    ```

### Changed

 - Depreciated `stringify()` in favor of just using the built-in `str()`.

### Fixed

 - Addresses issue #25 (INI parser isn't converting back to string).

## 0.11.0 - 2020-08-07

### Added

- `ConfigFile` can now accept yaml and toml files as optional extra file types.
  As long as the extras (`yaml` and `toml`) are installed, those file types can also
  be used.

- `ConfigFile` can now be indexed into using an array notation to get, set, and delete keys.

- `path` property to `ConfigFile`

- `original_path` property to `ConfigFile`

- `wild` optional argument to `has` on `ConfigFile` to check if the file has an
  occurrence of the key anywhere in the file.

### Removed

- `BaseParser` from the public API.

- `parser` optional argument from the `ConfigFile` constructor.

### Changed

- `path` on the `ConfigFile` is now a property that can only be retrieved. `contents` is now private
  but you can use `.stringify()` instead to get the contents. `parser` is now also private.

- `restore_original` in `ConfigFile` now raises a `FileNotFoundError` instead of an `OSError` if the original
  file path does not exist.

- `restore_original`'s optional argument is now called `original_path` rather than `original_file_path`.

### Fixed

- `default` in `ConfigFile`'s `get` method can now be `None`. Previously, it was defaulted to the
  value `None` so there was no way of distinguishing between the default value and a user inputted
  value of `None`.

## 0.10.0 - 2020-05-10

### Changed

- `toml` and `pyyaml` are now optional extra dependencies. This allows you to
  not have to install them if you aren't using them.

- `retrieve_all` in `JsonParser`'s `get` method is now called `get_all` for
  consistency. It isn't publicly available yet. The thought is to write a custom
  ini parser first that supports multiple of the same keys and subsections.
  This way you can have the `get_all`, `set_all`, `delete_all`, etc. methods
  for all file type parsers. I would have to weight if that added complexity
  of not using the built-in configparser and roll our own for some added
  features is worth it or see if there are ways to work around it with
  configparser that are ideal.

### Fixed

- You can now specify a default and still coerce your return type. Previously,
  if you specified a default, there was no logic in that branch to coerce your
  return type as well.

## 0.9.0 - 2020-02-09

### Added

- `default` optional parameter to the `get()` method of `ConfigFile`.
  The allows a default value to be fallen back to if the given key is missing.

- `return_type` optional parameter to `get()` method of `ConfigFile`. This
  allows you to coerce the return type to one of your choosing by feeding it
  the return value.

### Changed

- Automatic type parsing is now off by default. This is because of the addition of
  the `return_type` optional parameter. After using the package more, I think
  the explicitness of specifying the type you're after or that you'd like to
  automatically parse the type to one of the basic types is more maintainable.
  However, I think the option to automatically parse or parse a whole section of
  values is still a useful one.

- The `parse_type` parameter to `ConfigFile`'s `get()` method is now called
  `parse_types`.

## 0.8.0 - 2020-02-02

### Added

- More type hints to `ConfigFile` and `IniParser`.
- `nested_lookup` dependency to help with modifying deeply nested structures
  (JSON + YAML)
- `JsonParser` so you can now specify `.json` files to be parsed.

### Changed

- The original content of the passed in file is now called `content`
  instead of `contents`. This is for consistency since the parsed version is
  called `parsed_content`.

## 0.7.0 - 2020-01-27

### Fixed

- Support for using custom parsers with `ConfigFile` with the `parser` optional
  argument. This was technically supported before, but it was not tested and found
  to not actually use the passed in parser once tested.

### Changed

- The `reset()` method on `ConfigFile` is now called `restore_original()`.
  The behavior is the same. This was done to better describe what exactly that method
  is doing. Since the file is not written back out with every `set()` or `delete()`
  and calling `save()` explicitly is required, `reset()` may have been confused with
  resetting the changes you've made rather than deleting and restoring the original
  configuration file.

## 0.6.0 - 2020-01-24

### Changed

- Bumped down python version requirement to 3.6 and now test 3.6, 3.7, and 3.8 on CI.

## 0.5.0 - 2020-01-19

### Added

- Support for retrieving entire sections as a `dict` with `get()`.

## 0.4.0 - 2020-01-19

### Added

- `reset()` and `save()` methods to `ConfigFile`. This allows you to reset your
  configuration file to an "original state," given the original config file path.
  However, say you have a `config/config.json` file. Then it will automatically try
  to look for `config/config.original.json` if no file path is specified. The `save()`
  method should be called after your changes to the config file. It will write them
  back out.

- Raise test coverage to 93%.

## 0.3.3 - 2020-01-18

### Changed

- `_split_on_dot` is no longer in base parser (now in a utils file). Also, the default
  behavior is now to split on every dot and split on only the last dot if specified

### Fixed

- `ConfigFile` was trying to use `_split_on_dot`, but it no longer inherited from base parser.

- `TypeError` when setting the key/value pairs since configparser requires the option
  to be a string. The parser now just converts the value to a string if it is not one
  and then adds the key/value pair. It would still be parsed correctly when retrieving
  it.

## 0.3.1 - 2020-01-17

### Fixed

- `isinstance` call for `BaseParser` to be correctly used.

## 0.3.0 - 2020-01-17

### Added

- Abstract base parser as a contract for concrete file format parser implementations.

- Exposed `ConfigFile`, `BaseParser`, and `ParsingError` to the Public API. The base
  parser is exposed to allow future custom extensions of the config file and what it
  can parse by its users.

- `has_section` and `has_key` is now changed to a single `has` method which determines
  whether you're checking a section or key by the presence of a dot.

- `IniParser` to support the ini format. It uses configparser internally, but it is
  only exposed through the `ConfigFile` object.

## 0.2.0 - 2020-01-04

### Added

- Parsing of strings to their native values

## 0.1.0 - 2020-01-04

  - Initial Release