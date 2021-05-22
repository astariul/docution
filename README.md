<h1 align="center">docution</h1>
<p align="center">Host your API reference on Notion.</p>

<p align="center"><a href="https://github.com/astariul/docution/actions"><img src="https://github.com/astariul/docution/workflows/tests/badge.svg" alt="test status" /></a></p>

<h2 align="center">Install</h2>

Simply run :

```console
pip install git+https://github.com/astariul/docution.git
```

<h2 align="center">Example</h2>

Run :

```console
python -c "from docution import replace; replace(path='example')"
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

<h2 align="center">Unsupported</h2>

A few things are not supported yet by the official Notion API, and will need to be added in the future :


- [ ] **Deletion of the cmd block (`/docution my_module` for example).** For now the API doesn't support deletion, so we can't remove these blocks. Later it should be removed.
- [ ] **Add dividers.** Dividers are needed to have cleaner outputs. For now the API supports only text-based blocks, so we can't do that.
- [ ] **Remove recursion.** To access all the blocks of a page, we need to recursively call the API, for each children of children of children of ... This is inefficient. Later we should reduce that number of calls and just call the API once, retrieve everything, create everything, update the content with 1 call.
