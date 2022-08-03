import pathlib

from setuptools import setup, find_packages

readme_path = pathlib.Path("README.md")

setup(
    name='MyModule',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    url=' ',
    author=' ',
    author_email=' ',
    description='Some example used in my python development template repository.',
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5"
)
