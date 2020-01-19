# Contributing to Config File

The preferred workflow is via pull requests for code changes.

If you find a bug or want to suggest an improvement, etc., please open a issue.
This will make sure we notice it. You're also welcome to submit a pull request in this repository.

Here are some guidelines to keep in mind when submitting a pull request:

- Commit history: Try to keep a clean commit history so it is easier to
  see your changes. Keep functional changes and refactorings in separate commits.

- Commit messages: Have a short one line summary of your change followed by as many
  paragraphs of explanation as you need. This is the place to clarify any subtleties
  you have in your implemeƒntation, document other approaches you tried that didn't
  end up working, any limitations on your implementation, etc. The most important
  part here is to describe *why* you made the change you did, not simply *what* the
  change you made is.

- Changelog: Please ensure to update the changelog by adding a new bullet under
  an ``Added``, ``Changed``, ``Deprecated``, ``Removed``, ``Fixed``, or ``Security`` section
  headers under the ``Unreleased`` version. If any of those sections are not present,
  feel free to add the one you need. See
  [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) if you need guidance
  on what makes a good entry since this project follows those principles. If you're
  not comfortable with your English, we'd be happy to write it for you.

- Ensure the tests pass: ``poetry run pytest tests/`` to run all tests.
    - If you'd like to run with test coverage, pass ``--cov=config_file/`` to pytest.

- New features should be accompanied with tests for them:
  - Unit tests are written using [pytest](https://docs.pytest.org/en/latest/).

- Pre-commit pipeline: We use a pre-commit pipeline to ensure standard code format.

   - Unused imports are automatically removed using `autoflake <https://github.com/myint/autoflake>`_
   
   - The remaining imports are sorted using `isort <https://github.com/timothycrosley/isort>`_. 
   
   - All code is automatically formatted with `black <https://github.com/psf/black>`_ 
   
   - Lastly, everything is checked by `flake8 <https://gitlab.com/pycqa/flake8>`_. 
   
   Make sure to install pre-commit before making commits.

  Note: if any of the items had to do any reformatting, sorting, etc., the commit will
  fail. You'll have to re-add the items it fixed and try again.

  ```bash
    pre-commit install
  ```
  
- CI Pipeline: There is a CI pipeline that is run by Travis CI on commits to master and
  on pull requests.
  
  - All it does is ensure that all the tests pass and that all the files adhere to the 
    standard format (`pre-commit run --all-files`).

To get started, make sure you have poetry installed and run ``poetry install`` and
``poetry shell`` to enter the virtual environment.