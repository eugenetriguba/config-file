# Contributing to Config File

The preferred workflow is via pull requests for code changes.

If you find a bug or want to suggest an improvement, etc., please open a issue.
This will make sure it gets noticed. You're also welcome to submit a pull request in this repository.

Here are some guidelines to keep in mind when submitting a pull request:

- Commit history: Try to keep a clean commit history so it is easier to
  see your changes. Keep functional changes and refactorings in separate commits.

- Commit messages: Have a short one line summary of your change followed by as many
  paragraphs of explanation as you need. This is the place to clarify any subtleties
  you have in your implemeƒntation, document other approaches you tried that didn't
  end up working, any limitations on your implementation, etc. The most important
  part here is to describe _why_ you made the change you did, not simply _what_ the
  change you made is.

- Changelog: Please ensure to update the changelog by adding a new bullet under
  an `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security` section
  headers under the `Unreleased` version when applicable. If any of those sections
  are not present, feel free to add the one you need. See
  [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) if you need guidance
  on what makes a good entry since this project follows those principles.

- Ensure the tests pass: `poetry run task test` to run all tests.

- New features should be accompanied with tests for them:

  - Unit tests are written using [pytest](https://docs.pytest.org/en/latest/).

- Pre-commit pipeline: There is a pre-commit pipeline to enforce standard code format.

  Make sure to install pre-commit before making commits.

  ```
  $ pre-commit install
  ```

  Note: if any of the items had to do any reformatting, sorting, etc., the commit will
  fail. You'll have to re-add the items it fixed and try again.

- CI Pipeline: There is a CI pipeline that is run on commits and pull requests that
  ensures the tests pass.

To get started, make sure you have poetry installed and run `poetry install -E yaml -E toml` and `poetry shell` to enter the virtual environment.
