from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in i3/__init__.py
from i3 import __version__ as version

setup(
	name="i3",
	version=version,
	description="i3",
	author="Narayanan",
	author_email="narayanan.m@groupteampro.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
