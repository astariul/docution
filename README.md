<h1 align="center">docution</h1>
<p align="center">
Host your documentation easily on Notion
</p>

<p align="center">
    <a href="https://github.com/astariul/docution/releases"><img src="https://img.shields.io/github/release/astariul/docution.svg" alt="GitHub release" /></a>
    <a href="https://github.com/astariul/docution/actions/workflows/pytest.yaml"><img src="https://github.com/astariul/docution/actions/workflows/pytest.yaml/badge.svg" alt="Test status" /></a>
    <a href="https://github.com/astariul/docution/actions/workflows/lint.yaml"><img src="https://github.com/astariul/docution/actions/workflows/lint.yaml/badge.svg" alt="Lint status" /></a>
    <img src=".github/badges/coverage.svg" alt="Coverage status" />
    <a href="https://astariul.github.io/docution"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https%3A%2F%2Fastariul.github.io%2Fdocution" alt="Docs" /></a>
    <a href="https://github.com/astariul/docution/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#install">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#faq">FAQ</a> •
  <a href="#contribute">Contribute</a>
  <br>
  <a href="https://astariul.github.io/docution/" target="_blank">Documentation</a>
</p>


<h2 align="center">Description</h2>

**`docution`** is a small package to help you host your documentation on Notion.

The goal is to have a drop-in replacement of [`MkDocs`](https://www.mkdocs.org/) (so you can easily switch between them, according to your needs).

---

The two main advantages of hosting your documentation on Notion is that it's **free**, and you can have a **private documentation** (pages in Notion are private by default).

`docution` provides the following features :

* 🐣 Easy-to-use command line to deploy your documentation in Notion
* :octocat: Github actions for Continuous Deployment


<h2 align="center">Install</h2>

Install `docution` by running :


```
pip install docution
```

---

For development, you can install it locally by first cloning the repository :

```
git clone https://github.com/astariul/docution.git
cd docution
pip install -e .
```


<h2 align="center">Usage</h2>

_TODO_


<h2 align="center">FAQ</h2>

#### ❓ **What is `docution` compared to MkDocs ?**

MkDocs generates a static website from your documentation with Markdown files.

`docution` is just an alternative that uploads your documentation (with Markdown files) as a Notion page.

#### ❓ **Why should I use `docution` ?**

The advantages of uploading your documentation as a Notion page are multiple :

* No hassle to host a generated static website
* Free hosting (at least within the free tier offered by Notion)
* Private documentation (like any Notion page, possibility to manage access on a user-by-user basis) 


<h2 align="center">Contribute</h2>

To contribute, install the package locally, create your own branch, add your code (and tests, and documentation), and open a PR !

### Pre-commit hooks

Pre-commit hooks are set to check the code added whenever you commit something.

If you never ran the hooks before, install it with :

```bash
pre-commit install
```

---

Then you can just try to commit your code. If you code does not meet the quality required by linters, it will not be committed. You can just fix your code and try to commit again !

---

You can manually run the pre-commit hooks with :

```bash
pre-commit run --all-files
```

### Tests

When you contribute, you need to make sure all the unit-tests pass. You should also add tests if necessary !

You can run the tests with :

```bash
pytest
```

---

Tests are not included in the pre-commit hooks, because running the tests might be slow, and for the sake of developpers we want the pre-commit hooks to be fast !

Pre-commit hooks will not run the tests, but it will automatically update the coverage badge !

### Documentation

The documentation should be kept up-to-date. You can visualize the documentation locally by running :

```bash
mkdocs serve
```
