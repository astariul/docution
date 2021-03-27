import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fr:
    reqs = fr.read().strip().split('\n')


setuptools.setup(
    name="docution",
    version="0.1",
    author="Nicolas REMOND",
    author_email="nicolas@remond.co",
    description="Host your API reference on Notion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astariul/docution",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=reqs,
)
