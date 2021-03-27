<h1 align="center">docution</h1>
<p align="center">Host your API reference on Notion.</p>

<p align="center"><a href="https://github.com/astariul/docution/actions"><img src="https://github.com/astariul/docution/workflows/tests/badge.svg" alt="test status" /></a></p>

<h2 align="center">Install</h2>

Simply run :

```console
pip install git+https://github.com/astariul/docution.git
```

<h2 align="center">Contribute</h2>

Ensure tests are passing :

```console
pip install pytest

python -m pytest -W ignore::DeprecationWarning
```

---

Check if code is well-formated :

```console
pip install flake8

flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```
