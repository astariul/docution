import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


reqs = []

extras_require = {
    "test": ["pytest~=7.0", "pytest-cov~=3.0", "coverage-badge~=1.0"],
    "hook": ["pre-commit~=2.15"],
    "lint": ["isort~=5.9", "black~=22.1", "flake518~=1.2", "darglint~=1.8"],
    "docs": ["mkdocs-material~=8.1", "mkdocstrings[python]~=0.18", "mike~=1.1"],
}
extras_require["all"] = sum(extras_require.values(), [])
extras_require["dev"] = (
    extras_require["test"] + extras_require["hook"] + extras_require["lint"] + extras_require["docs"]
)

setuptools.setup(
    name="docution",
    version="1.0.0.dev0",
    author="Nicolas REMOND",
    author_email="remondnicola@gmail.com",
    description="Host your documentation easily on Notion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astariul/docution",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=reqs,
    extras_require=extras_require,
)
