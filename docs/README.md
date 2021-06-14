# Documentation

First, install `sphinx` and the theme :

```console
pip install sphinx sphinx_rtd_theme
```

You can then generate documentation with following command :

```console
cd docs
make html
```

---

On Windows, you can generate it with :

```console
C:\Users\<username>\AppData\Roaming\Python\Python39\Scripts\sphinx-build docs docs/_build/html
```

---

Documentation is generated in the folder `docs/_build/html/`.

You can just open `docs/_build/html/index.html` in your browser.

To open a server serving the documentation, do :

```console
cd docs/_build/html/
python3 -m http.server 8800
```