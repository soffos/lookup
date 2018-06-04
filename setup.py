from setuptools import setup

with open("README.md", 'r') as f:
  readme = f.read()

setup(
  name="lookup",
  version="1.0.0",
  description="Module for extracting IPv4 addresses from a text file and performing GeoIP/RDAP lookups",
  license="MIT",
  long_description=readme,
  author="Chris Soffos",
  author_email="csoffos@gmail.com",
  packages=['lookup'],
  install_requires=[
    'flask',
    'requests'
  ],
)