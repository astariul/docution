<p align="center">
    <img src="https://user-images.githubusercontent.com/43774355/122676145-9b81fc00-d217-11eb-91fe-949964642c35.png">
</p>
<p align="center"><b>🚧 This is an <i>alpha</i> version of the project, a proof of concept. Looking for collaborators !</b></p>
<p align="center">Bring autodoc capabilities to your Notion workspace with Docution</p>

<p align="center">
    <a href="https://github.com/astariul/docution/actions"><img src="https://github.com/astariul/docution/workflows/tests/badge.svg" alt="test status" /></a>
    <a href="https://github.com/astariul/docution/releases"><img src="https://img.shields.io/github/v/release/astariul/docution" alt="release" /></a>
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#install">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#faq">FAQ</a> •
  <a href="#contribute">Contribute</a> •
  <a href="#roadmap">Roadmap</a>
  <br>
  <a href="https://www.notion.so/Documentation-bb693b18c3b1433ca076eec9fcb8a2db" target="_blank">Documentation</a>
</p>

<h2 align="center">Description</h2>

Writing documentation in Notion is an attractive alternative to other solutions :

- ✨ Neat interface, rich text editing
- 👥 Easy to share and collaborate, while keeping it private
- 🚀 Already hosted !

But Notion lacks features that makes the power of other solutions, like auto-documentation ! This is the role of **`docution`** : a python package and command line that updates your Notion pages with clean formatted documentation.

<h2 align="center">Install</h2>

Simply run :

```console
pip install docution
```

<h2 align="center">Usage</h2>

In your Notion page, create a text block like follow :

```console
/docution my_module.my_function
```

After creating your integration and giving it access to your page, just run :

```console
docution --auth_token <secret> --page_id <id>
```

And here you go ! Your Notion page is updated with your documentation :

![](https://user-images.githubusercontent.com/43774355/122676911-fec15d80-d21a-11eb-8f83-94e467dff43a.png)

----

You can check the `docution` usage with :

```console
docution --help
```

**Please also check the [documentation](https://www.notion.so/Get-started-6df1da88e24c4d3391e94e105e85c9a0) for a full example with all the details !**

<h2 align="center">FAQ</h2>

#### **Why is it in alpha ?**

Currently, the official Notion API is in _beta_, which means it can change anytime.

Also, this project needs additional features that are not implemented in the Notion API yet to be fully functional. So for now, this is just a proof of concept.

Checkout the [current limitations](https://www.notion.so/Limitations-3ebb3d37a9754f56b2e057b1e255e520) for more details.

#### **How does it work ?**

When you use the `docution` command line, the following happens :

* Retrieve all the blocks used in the Notion page with the given ID
* Detect the blocks that are a docution command (`/docution a.b.c`)
* Import the docstring of the object `a.b.c`
* Correctly format the docstring as Notion blocks
* Write these blocks in your Notion page 

<h2 align="center">Contribute</h2>

Clone the repository locally, create your branch, push your changes and open a PR !

---

Check if code is well-formated :

```console
pip install flake8

flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

<h2 align="center">Roadmap</h2>

* Add missing functionality to be similar to sphinx (document public methods of class, etc...)

* Add option to specify path of module
* Add option for private members, only specific member, etc...
* Should we add the module name (when documenting module) ? Add option for that ?
* Should we add only the name of the thing, or the whole path ? Add option for that ?
* Add option for dryrun
* Change parser to `pardoc` ? To handle other type of section, like `Example`.
* Optimize API call to NOT do recursive calling (for now, no choice)
* Handle markdown ?
* Handle RST ?
