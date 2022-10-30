# Docution

## Introduction

Welcome to the documentation of the `docution` package.

**`docution`** is a small package to help you host your documentation on Notion.

The goal is to have a drop-in replacement of [`MkDocs`](https://www.mkdocs.org/) (so you can easily switch between them, according to your needs).

To learn more on how to use `docution`, check out the [Usage](usage.md) page.

## Installation

### Latest version

You can install the latest version of the package directly from PyPi with :

```bash
pip install docution
```

!!! hint
    If you want to install directly from Github, run :
    ```bash
    pip install git+https://github.com/astariul/docution.git
    ```

### Specific version

You can install a specific version of the package (`0.1.0` in ths example) from PyPi with :

```bash
pip install docution==0.1.0
```

!!! hint
    If you want to install directly from Github, run :
    ```bash
    pip install git+https://github.com/astariul/docution.git@v0.1.0
    ```

### Local

You can also clone the repository locally and install it manually :

```bash
git clone https://github.com/astariul/docution.git
cd docution
pip install -e .
```

### Extra dependencies

You can also install extras dependencies, for example :

```bash
pip install -e .[docs]
```

Will install necessary dependencies for building the docs.

!!! hint
    If you installed the package directly from github, run :
    ```bash
    pip install "docution[docs] @ git+https://github.com/astariul/docution.git"
    ```

---

List of extra dependencies :

* **`test`** : Dependencies for running unit-tests.
* **`hook`** : Dependencies for running pre-commit hooks.
* **`lint`** : Dependencies for running linters and formatters.
* **`docs`** : Dependencies for building the documentation.
* **`dev`** : `test` + `hook` + `lint` + `docs`.
* **`all`** : All extra dependencies.

## Contribute

To contribute, install the package locally (see [Installation](#local)), create your own branch, add your code (and tests, and documentation), and open a PR !

### Pre-commit hooks

Pre-commit hooks are set to check the code added whenever you commit something.

When you try to commit your code, hooks are automatically run, and if you code does not meet the quality required by linters, it will not be committed. You then have to fix your code and try to commit again !

!!! important
    If you never ran the hooks before, install it with :
    ```bash
    pre-commit install
    ```

!!! info
    You can manually run the pre-commit hooks with :
    ```bash
    pre-commit run --all-files
    ```

### Unit-tests

When you contribute, you need to make sure all the unit-tests pass. You should also add tests if necessary !

You can run the tests with :

```bash
pytest
```

!!! info
    Tests are not included in the pre-commit hooks, because running the tests might be slow, and for the sake of developpers we want the pre-commit hooks to be fast !

!!! info
    Pre-commit hooks will not run the tests, but it will automatically update the coverage badge !

### Documentation

When you contribute, make sure to keep the documentation up-to-date.

You can visualize the documentation locally by running :

```bash
mkdocs serve
```
